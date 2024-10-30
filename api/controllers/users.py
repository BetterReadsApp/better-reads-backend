from fastapi import APIRouter, Depends, Header, HTTPException, Path
from sqlmodel import Session
from ..db import get_session, get_user_by_field
from ..model.user import UserPublic, UserPrivate
from typing import Annotated, Union

router = APIRouter(prefix="/users", tags=["Users"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"


@router.get("/{user_id}", response_model=Union[UserPrivate, UserPublic])
def get_user_by_id(
    user_id: int = Path(description="Id del usuario que **quiero obtener**"),
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", user_id, session)
    if auth == user_id:
        return user
    return UserPublic.from_private(user, auth_user_id=auth)


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
