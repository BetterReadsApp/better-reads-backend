from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from api.db import get_session, get_user_by_field, user_exists_by_field
from api.model.user import UserFormLogin, UserFormRegister, User
import bcrypt
import re


router = APIRouter(tags=["Auth"])
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w-]+\.[\w-]{2,}$")
MIN_PASSWORD_LENGTH = 8
DEFAULT_AVATAR = "https://api.dicebear.com/9.x/adventurer/svg?seed=Alexander"


@router.post("/login")
def log_user_in(user_form: UserFormLogin, session: Session = Depends(get_session)):
    user = get_user_by_field("email", user_form.email, session)
    if not bcrypt.checkpw(
        user_form.password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"user_id": user.id}


@router.post("/register")
def register_user(user_form: UserFormRegister, session: Session = Depends(get_session)):
    if len(user_form.password) < MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Password must have {MIN_PASSWORD_LENGTH} characters",
        )
    if not EMAIL_REGEX.match(user_form.email):
        raise HTTPException(status_code=400, detail="Email domain is not allowed")
    if user_exists_by_field("email", user_form.email, session):
        raise HTTPException(status_code=400, detail="Email is already in use")

    user = User.model_validate(user_form)
    hashed_password = bcrypt.hashpw(
        user_form.password.encode("utf-8"), bcrypt.gensalt()
    )
    user.password = hashed_password.decode("utf-8")
    user.is_author = user_form.is_author
    user.avatar_image_url = DEFAULT_AVATAR
    user.set_default_shelves()

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
