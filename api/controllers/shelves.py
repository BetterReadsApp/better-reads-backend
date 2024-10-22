from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from ..db import get_session, user_exists_by_field
from ..model.shelf import ShelfForm, Shelf

router = APIRouter(tags=["Shelves"])


@router.post("/shelves")
def create_shelf(
    shelf_form: ShelfForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header()] = None,
):
    shelf = Shelf.model_validate(shelf_form)
    shelf.user_id = auth

    if not user_exists_by_field("id", shelf.user_id, session):
        raise HTTPException(status_code=404, detail="User not found")

    session.add(shelf)
    session.commit()
    session.refresh(shelf)

    return shelf
