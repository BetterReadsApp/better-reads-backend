from fastapi import APIRouter, Depends, Header, HTTPException, Path, Query
from sqlmodel import Session
from api.db import get_book_by_id, get_books, get_books_by_authors, get_books_by_genre, get_rated_books_by_user_id, get_read_books_by_user_id, get_session, get_user_by_field, get_users_by_name_and_last_name
from api.model.book import Book
from api.model.user import UserPublic, UserPrivate, UserMini
from typing import Annotated, Union

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


@router.get("/{user_id}", response_model=Union[UserPrivate, UserPublic])
def get_user_by_id(
    user_id: int = Path(description="Id del usuario que **quiero obtener**"),
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", user_id, session)
    my_user = get_user_by_field("id", auth, session)
    user_converter = (
        UserPublic.from_user if my_user.id != user.id else UserPrivate.from_user
    )
    return user_converter(user, auth)


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


@router.get("/{user_id}/recommendations", response_model=list[Book])
def get_book_recommendations(
    user_id: int = Path(description="Id del usuario que **quiere libros recomendados**"),
    session: Session = Depends(get_session),
):
    user = get_user_by_field("id", user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    final_list = []
    rated_books = get_rated_books_by_user_id(user_id, session)
    if rated_books:
        well_rated_books = filter_by_rating(rated_books, user_id)
        final_list.extend(find_recommended_books(well_rated_books, session))
    
    read_books = get_read_books_by_user_id(user_id, session)
    if len(final_list) < 7 and read_books:
        final_list.extend(find_recommended_books(read_books, session))
    
    if len(final_list) < 7:
        final_list.extend(get_books(session))

    return final_list
    

def find_recommended_books(books: list[Book], session: Session = Depends(get_session)):
    final_list = []
    book_authors = get_books_by_authors(books, session)
    book_genres = get_books_by_genre(books, session)

    final_list.extend(book_authors)
    final_list.extend(book_genres)
    return final_list


def filter_by_rating(books: list[Book], user_id: int):
    well_rated_books = []
    for book in books:
        for rating in book.ratings:
            if rating.user_id == user_id and rating.value >= 3:
                well_rated_books.append(book)
    return well_rated_books
