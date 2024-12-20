from fastapi import APIRouter, Depends, Header, HTTPException, Path, Query
from sqlmodel import Session
from api.controllers.auth import EMAIL_REGEX
from api.db import (
    get_session,
    get_user_by_field,
    get_users_by_name_and_last_name,
    user_exists_by_field,
)
from api.model.enums.avatar import Avatar
from api.model.user import UserMini, UserUpdate
from api.formatters.user_formatter import UserFormatter
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"


@router.get("", response_model=list[UserMini])
def get_users(
    name: str = Query(None, description="Nombre del usuario **que quiero obtener**"),
    last_name: str = Query(
        None, description="Apellido del usuario **que quiero obtener**"
    ),
    session: Session = Depends(get_session),
):
    return get_users_by_name_and_last_name(name, last_name, session)


@router.get("/{user_id}")
def get_user_by_id(
    user_id: int = Path(description="Id del usuario que **quiero obtener**"),
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", user_id, session)
    my_user = get_user_by_field("id", auth, session)
    return UserFormatter.format_for_user(user, my_user)


@router.post("/{user_id}/followers")
def follow_user(
    user_id: int = Path(description="Id del usuario que **quiero seguir**"),
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    if auth == user_id:
        raise HTTPException(status_code=403, detail="You cannot follow yourself")

    follower_user = get_user_by_field("id", auth, session)
    to_be_followed_user = get_user_by_field("id", user_id, session)

    if follower_user.is_following(to_be_followed_user):
        raise HTTPException(
            status_code=409, detail="You're already following that user"
        )

    follower_user.follow(to_be_followed_user)
    session.add(follower_user)
    session.commit()
    return {"detail": "User followed successfully"}


@router.delete("/{user_id}/followers")
def unfollow_user(
    user_id: int = Path(description="Id del usuario que **quiero dejar de seguir**"),
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    if auth == user_id:
        raise HTTPException(status_code=403, detail="You cannot unfollow yourself")

    follower_user = get_user_by_field("id", auth, session)
    to_be_unfollowed_user = get_user_by_field("id", user_id, session)

    if not follower_user.is_following(to_be_unfollowed_user):
        raise HTTPException(status_code=409, detail="You aren't following that user")

    follower_user.unfollow(to_be_unfollowed_user)
    session.add(follower_user)
    session.commit()
    return {"detail": "User unfollowed successfully"}


@router.put("/{user_id}")
def edit_user_profile(
    new_user: UserUpdate,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", auth, session)

    if not EMAIL_REGEX.match(new_user.email):
        raise HTTPException(status_code=400, detail="Email domain is not allowed")
    if (
        user_exists_by_field("email", new_user.email, session)
        and new_user.email != user.email
    ):
        raise HTTPException(status_code=400, detail="Email is already in use")

    if user.is_author and not new_user.is_author:
        raise HTTPException(status_code=409, detail="You cannot stop being an author")

    if new_user.avatar_image_url not in [avatar.value for avatar in Avatar]:
        raise HTTPException(status_code=400, detail="Invalid avatar URL")

    user.name = new_user.name
    user.last_name = new_user.last_name
    user.email = new_user.email
    user.is_author = new_user.is_author
    user.avatar_image_url = new_user.avatar_image_url

    session.commit()
    session.refresh(user)
    return UserFormatter.format_for_user(user, user)
