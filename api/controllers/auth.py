from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from ..db import get_session, get_user_by_email, user_exists_by_field
from ..model.user import UserForm, User, UserBase
from ..model.shelf import Shelf
import bcrypt

router = APIRouter(tags=["Auth"])


@router.post("/login")
def log_user(user_base: UserBase, session: Session = Depends(get_session)):
    user = get_user_by_email(user_base.email, session)

    if not bcrypt.checkpw(
        user_base.password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"user_id": user.id}


@router.post("/register")
def create_user(user_form: UserForm, session: Session = Depends(get_session)):
    if user_exists_by_field("email", user_form.email, session):
        raise HTTPException(status_code=400, detail="Email is already in use")

    hashed_password = bcrypt.hashpw(
        user_form.password.encode("utf-8"), bcrypt.gensalt()
    )
    user_form.password = hashed_password.decode("utf-8")
    new_user = User.model_validate(user_form)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    shelves = create_default_shelves(new_user.id)

    session.add_all(shelves)
    session.commit()
    session.refresh(new_user)

    return {"user_id": new_user.id}


def create_default_shelves(user_id: int) -> list[Shelf]:
    shelf_names = ["Currently Reading", "Read", "To Read"]
    return [Shelf(name=name, user_id=user_id) for name in shelf_names]
