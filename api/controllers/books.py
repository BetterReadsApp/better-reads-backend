from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session, get_book_by_id
from ..model.book import BookForm, Book

router = APIRouter(tags=["Books"])


@router.get("/books")
def get_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@router.get("/books/{book_id}")
def get_book(book_id, session: Session = Depends(get_session)):
    return get_book_by_id(book_id, session)


@router.post("/books")
def create_book(book_form: BookForm, session: Session = Depends(get_session)):
    # session.add(book_form)
    # session.commit()
    # session.refresh(book_form)
    return book_form
