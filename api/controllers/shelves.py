from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from ..db import get_session, user_exists_by_field, get_book_by_id, get_shelf_by_id
from ..model.shelf import ShelfForm, Shelf, ShelfPrivate, ShelfPublic

router = APIRouter(prefix="/shelves", tags=["Shelves"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"


@router.get("", response_model=Union[list[Shelf], list[ShelfPrivate]])
def get_shelves(
    name: str | None = None,
    user_id: int | None = None,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    query = select(Shelf)
    query = query.where(Shelf.name == name) if name else query
    query = query.where(Shelf.user_id == user_id) if user_id else query
    shelves = session.exec(query).all()
    if name and user_id and (user_id == auth):
        shelves = [ShelfPrivate.model_validate(shelves[0])]
    return shelves


@router.post("")
def create_shelf(
    shelf_form: ShelfForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    shelf = Shelf.model_validate(shelf_form)
    shelf.user_id = auth

    if not user_exists_by_field("id", shelf.user_id, session):
        raise HTTPException(status_code=404, detail="User not found")

    query = (
        select(Shelf)
        .where(Shelf.name == shelf.name)
        .where(Shelf.user_id == shelf.user_id)
    )
    shelf_exists = session.exec(query).first() is not None
    if shelf_exists:
        raise HTTPException(
            status_code=400, detail="You already have a shelf with that name"
        )

    session.add(shelf)
    session.commit()
    session.refresh(shelf)
    return shelf


@router.get("/{shelf_id}", response_model=Union[ShelfPrivate, ShelfPublic])
def get_shelf(
    shelf_id: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    shelf = get_shelf_by_id(shelf_id, session)
    if shelf.user_id == auth:
        return shelf
    return ShelfPublic.model_validate(shelf)


@router.post("/{shelf_id}/books", response_model=ShelfPrivate)
def add_book_to_shelf(
    shelf_id: int,
    book_id: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    shelf = session.exec(select(Shelf).where(Shelf.id == shelf_id)).first()
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")

    if shelf.user_id != auth:
        raise HTTPException(
            status_code=403, detail="You cannot add a book to a shelf that's not yours"
        )

    book = get_book_by_id(book_id, session)
    if shelf.contains(book):
        raise HTTPException(
            status_code=403, detail="The shelf already contains that book"
        )

    shelf.add(book)
    session.add(shelf)
    session.commit()
    session.refresh(shelf)
    return shelf
