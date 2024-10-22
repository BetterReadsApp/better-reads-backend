from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session, user_exists_by_field
from ..model.shelf import ShelfForm, Shelf

router = APIRouter(tags=["Shelves"])


@router.post("/shelves")
def create_shelf(shelf_form: ShelfForm, session: Session = Depends(get_session)):
    if not user_exists_by_field("id", shelf_form.user_id, session):
        raise HTTPException(status_code=404, detail="User not found")

    shelf = Shelf.model_validate(shelf_form)
    session.add(shelf)
    session.commit()
    session.refresh(shelf)

    return shelf
