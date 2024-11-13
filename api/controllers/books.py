from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlmodel import Session, select, or_, extract
from typing import Annotated
from api.db import (
    get_books_by_authors,
    get_books_by_genre,
    get_rated_books_by_user_id,
    get_read_books_by_user_id,
    get_session,
    get_book_by_id,
    get_user_by_field,
)
from api.model.enums.book_genre import BookGenre
from api.model.book import BookForm, Book, BookMini
from api.model.review import Review, ReviewForm
from api.model.rating import Rating, RatingForm
from api.model.quiz import QuizForm, Quiz
from api.model.question import Question
from api.model.user import User
from api.formatters.book_formatter import BookFormatter

router = APIRouter(tags=["Books"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"
MIN_QUESTIONS_PER_QUIZ = 1


@router.get("/books", response_model=list[BookMini])
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
        query = query.join(Book.author).where(
            or_(
                Book.title.icontains(keywords),
                User.name.icontains(keywords),
                User.last_name.icontains(keywords),
            )
        )
    if genre:
        query = query.where(Book.genre == genre)
    if from_year:
        query = query.where(from_year <= extract("year", Book.publication_date))
    if to_year:
        query = query.where(extract("year", Book.publication_date) <= to_year)

    return session.exec(query).all()


@router.get("/books/{book_id}")
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", auth, session) if auth else None
    book = get_book_by_id(book_id, session)
    return BookFormatter.format_for_user(book, user)


@router.post("/books")
def create_book(book_form: BookForm, session: Session = Depends(get_session)):
    user = get_user_by_field("id", book_form.author_id, session)
    if not user.is_author:
        raise HTTPException(
            status_code=403, detail="You must be an author to create a book"
        )
    book = Book.model_validate(book_form)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/books/{book_id}/reviews")
def get_reviews_for_book(book_id: int, session: Session = Depends(get_session)):
    book = get_book_by_id(book_id, session)
    return BookFormatter.format_reviews(book.reviews)


@router.post("/books/{book_id}/reviews")
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
        "review": review_form.review,
    }


@router.post("/books/{book_id}/ratings")
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


@router.get("/recommended", response_model=list[BookMini])
def get_recommended_books(
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
    session: Session = Depends(get_session),
):
    user = get_user_by_field("id", auth, session)

    final_list = []
    rated_books = get_rated_books_by_user_id(auth, session)
    if rated_books:
        well_rated_books = filter_by_rating(rated_books, auth)
        final_list.extend(find_recommended_books(well_rated_books, session))

    read_books = get_read_books_by_user_id(auth, session)
    if len(final_list) < 7 and read_books:
        for book in find_recommended_books(read_books, session):
            if book not in final_list:
                final_list.append(book)

    if len(final_list) < 7:
        for book in get_books(None, None, None, None, session):
            if book not in final_list:
                final_list.append(book)

    return [BookMini.model_validate(book) for book in final_list]


def find_recommended_books(books: list[Book], session: Session):
    final_set = []
    final_set.extend(get_books_by_authors(books, session))
    for book in get_books_by_genre(books, session):
        if book not in final_set:
            final_set.append(book)

    return list(final_set)


def filter_by_rating(books: list[Book], user_id: int):
    return [
        book
        for book in books
        if any(
            rating.user_id == user_id and rating.value >= 3 for rating in book.ratings
        )
    ]
