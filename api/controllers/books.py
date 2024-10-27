from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select
from ..db import get_session, get_book_by_id, get_user_by_field
from ..model.book import BookForm, Book, BookPublic
from ..model.rating import Rating
from typing import Annotated

router = APIRouter(prefix="/books", tags=["Books"])


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
    auth: Annotated[int, Header()] = None,
):
    if not 1 <= value <= 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be an integer between 1 and 5 (both included)",
        )

    user = get_user_by_field("id", auth, session)
    book = get_book_by_id(book_id, session)
    query = (
        select(Rating).where(Rating.user_id == user.id).where(Rating.book_id == book.id)
    )
    book_already_rated = session.exec(query).first() is not None
    if book_already_rated:
        raise HTTPException(status_code=400, detail="You've already rated this book")

    times_rated = session.query(Rating).filter(Rating.book_id == book.id).count()
    rating = Rating(value=value, user=user, book=book)
    rating.update_average(times_rated)
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating
