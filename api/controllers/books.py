from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlmodel import Session, select, or_, extract
from api.model.review import Review, ReviewForm
from api.db import get_session, get_book_by_id, get_user_by_field
from api.model.book import BookForm, Book, BookPublic, BookPrivate, BookMini
from api.model.rating import Rating, RatingForm
from api.model.enums.book_genre import BookGenre
from typing import Annotated, Union

router = APIRouter(prefix="/books", tags=["Books"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"


@router.get("", response_model=list[BookMini])
def get_books(
    keywords: str = Query(
        None, description="Palabras que coincidan con algún **título o autor**"
    ),
    from_year: int = Query(
        None, description="**Año** de publicación **desde** el que quiero obtener"
    ),
    to_year: int = Query(
        None, description="**Año** de publicación **hasta** el que quiero obtener"
    ),
    genre: BookGenre = Query(None, description="**Género**"),
    session: Session = Depends(get_session),
):
    query = select(Book)
    if keywords:
        query = query.where(
            or_(Book.title.icontains(keywords), Book.author.icontains(keywords))
        )
    if genre:
        query = query.where(Book.genre == genre)
    if from_year:
        query = query.where(from_year <= extract("year", Book.publication_date))
    if to_year:
        query = query.where(extract("year", Book.publication_date) <= to_year)

    return session.exec(query).all()


@router.get("/{book_id}", response_model=Union[BookPublic, BookPrivate])
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    book = get_book_by_id(book_id, session)
    if auth:
        user = get_user_by_field("id", auth, session)
        book = BookPrivate.from_book(book)
        book.load_info_for(user)
    else:
        book = BookPublic.from_book(book)
    return book


@router.post("")
def create_book(book_form: BookForm, session: Session = Depends(get_session)):
    book = Book.model_validate(book_form)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.post("/{book_id}/ratings")
def rate_book(
    book_id: int,
    rating_form: RatingForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    value = rating_form.value
    if not 1 <= value <= 5:
        raise HTTPException(
            status_code=400, detail="Rating must be an integer between 1 and 5"
        )

    user = get_user_by_field("id", auth, session)
    book = get_book_by_id(book_id, session)
    query = (
        select(Rating).where(Rating.user_id == user.id).where(Rating.book_id == book.id)
    )
    existing_rating = session.exec(query).first()

    if existing_rating:
        all_ratings = session.query(Rating).filter(Rating.book_id == book.id).all()
        total_ratings_count = len(all_ratings)
        total_ratings_value = (
            sum(rating.value for rating in all_ratings) - existing_rating.value
        )
        existing_rating.value = value
        total_ratings_value += value

        if total_ratings_count > 0:
            book.average_rating = total_ratings_value / total_ratings_count

    else:
        session.add(Rating(value=value, user=user, book=book))

        all_ratings = session.query(Rating).filter(Rating.book_id == book.id).all()
        total_ratings_count = len(all_ratings)
        total_ratings_value = sum(rating.value for rating in all_ratings) + value

        if total_ratings_count > 0:
            book.average_rating = total_ratings_value / (total_ratings_count + 1)

    session.commit()
    return {
        "status": "updated" if existing_rating else "created",
        "average_rating": book.average_rating,
    }


@router.post("/{book_id}/reviews")
def review_book(
    book_id: int,
    review_form: ReviewForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", auth, session)
    book = get_book_by_id(book_id, session)
    query = (
        select(Review).where(Review.user_id == user.id).where(Review.book_id == book.id)
    )
    existing_review = session.exec(query).first()

    if existing_review:
        existing_review.review = review_form.review
    else:
        session.add(Review(review=review_form.review, user=user, book=book))

    session.commit()
    return {
        "status": "updated" if existing_review else "created",
        "review description": review_form.review,
    }


@router.get("/{book_id}/reviews")
def get_reviews_for_book(book_id: int, session: Session = Depends(get_session)):
    book = get_book_by_id(book_id, session)
    return book.reviews


