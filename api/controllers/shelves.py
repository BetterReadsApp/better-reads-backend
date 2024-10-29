from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from ..db import get_session, user_exists_by_field
from ..model.shelf import ShelfForm, Shelf

router = APIRouter(prefix="/shelves", tags=["Shelves"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"


@router.get("")
def get_shelves(
    name: str | None = None,
    user_id: int | None = None,
    session: Session = Depends(get_session),
):
    print(f"NAME: {name}")
    query = select(Shelf)
    query = query.where(Shelf.name == name) if name else query
    query = query.where(Shelf.user_id == user_id) if user_id else query
    return session.exec(query).all()


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
