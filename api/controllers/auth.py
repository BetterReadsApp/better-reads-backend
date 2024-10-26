from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from ..db import get_session, get_user_by_field, user_exists_by_field
from ..model.user import UserFormLogin, UserFormRegister, User
from ..model.shelf import Shelf
import bcrypt
import re


router = APIRouter(tags=["Auth"])
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w-]+\.[\w-]{2,}$")


@router.post("/login")
def log_user(user_form: UserFormLogin, session: Session = Depends(get_session)):
    user = get_user_by_field("email", user_form.email, session)

    if not bcrypt.checkpw(
        user_form.password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"user_id": user.id}


@router.post("/register")
def create_user(user_form: UserFormRegister, session: Session = Depends(get_session)):
    if len(user_form.password) < 8:
        raise HTTPException(status_code=400, detail="Password must have 8 characters")
    if not EMAIL_REGEX.match(user_form.email):
        raise HTTPException(status_code=400, detail="Email domain is not allowed")
    if user_exists_by_field("email", user_form.email, session):
        raise HTTPException(status_code=400, detail="Email is already in use")

    hashed_password = bcrypt.hashpw(
        user_form.password.encode("utf-8"), bcrypt.gensalt()
    )
    user_form.password = hashed_password.decode("utf-8")
    new_user = User.model_validate(user_form)
    new_user.shelves = [
        Shelf(name="To Read"),
        Shelf(name="Currently Reading"),
        Shelf(name="Read"),
    ]

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"user_id": new_user.id}
