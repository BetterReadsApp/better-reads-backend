from fastapi import APIRouter, Depends, Header
from sqlmodel import Session
from ..db import get_session, get_user_by_field
from ..model.user import UserPublic, UserPrivate
from typing import Annotated, Union

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=Union[UserPrivate, UserPublic])
def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header()] = None,
):
    user = get_user_by_field("id", user_id, session)
    if auth == user_id:
        return user
    return UserPublic(
        id=user.id, name=user.name, last_name=user.last_name, email=user.email
    )
