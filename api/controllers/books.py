from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select
from ..db import get_session, get_book_by_id, get_user_by_field
from ..model.book import BookForm, Book, BookPublic
from ..model.rating import Rating
from typing import Annotated

router = APIRouter(prefix="/books", tags=["Books"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"


@router.get("")
def get_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@router.get("/{book_id}", response_model=BookPublic)
def get_book(book_id: int, session: Session = Depends(get_session)):
    return get_book_by_id(book_id, session)


@router.post("")
def create_book(book_form: BookForm, session: Session = Depends(get_session)):
    # session.add(book_form)
    # session.commit()
    # session.refresh(book_form)
    return book_form


@router.post("/{book_id}/ratings")
def rate_book(
    book_id: int,
    value: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
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
        existing_rating = Rating(value=value, user=user, book=book)
        session.add(existing_rating)

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
