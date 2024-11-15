from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .review import Review, ReviewedBook
from .shelf import Shelf, ShelfMini
from .rating import Rating, RatedBook
from .following import Following


class UserBase(SQLModel):
    name: str
    last_name: str
    email: str
    is_author: bool = Field(default=False, nullable=False)


class UserFormRegister(UserBase):
    password: str


class UserFormLogin(SQLModel):
    email: str
    password: str


class User(UserFormRegister, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    shelves: List[Shelf] = Relationship(back_populates="user")
    created_books: List["Book"] = Relationship(back_populates="author")
    rated_books: List[Rating] = Relationship(back_populates="user")
    reviewed_books: List[Review] = Relationship(back_populates="user")
    questions_answered: List["Answer"] = Relationship(back_populates="user")
    followers: List["User"] = Relationship(
        back_populates="following",
        link_model=Following,
        sa_relationship_kwargs={
            "primaryjoin": "User.id==Following.following_id",
            "secondaryjoin": "User.id==Following.follower_id",
        },
    )
    following: List["User"] = Relationship(
        back_populates="followers",
        link_model=Following,
        sa_relationship_kwargs={
            "primaryjoin": "User.id==Following.follower_id",
            "secondaryjoin": "User.id==Following.following_id",
        },
    )

    def follow(self, user):
        self.following.append(user)

    def unfollow(self, user):
        self.following.remove(user)

    def is_following(self, user):
        return user in self.following

    def __eq__(self, other):
        return self.id == other.id

    def set_default_shelves(self):
        self.shelves = [
            Shelf(name="To Read"),
            Shelf(name="Currently Reading"),
            Shelf(name="Read"),
        ]


class UserMini(SQLModel):
    id: int
    name: str
    last_name: str


class UserPrivate(UserBase):
    id: int
    is_author: bool
    shelves: List[ShelfMini] = []
    rated_books: List[RatedBook] = []
    reviewed_books: List[ReviewedBook] = []
    followers: List[UserMini] = []
    following: List[UserMini] = []

    @classmethod
    def from_user(cls, user: User, auth_user_id: int):
        rated_books = list(map(RatedBook.from_rating, user.rated_books))
        reviewed_books = list(map(ReviewedBook.from_review, user.reviewed_books))

        return cls(
            id=user.id,
            is_author=user.is_author,
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            shelves=user.shelves,
            rated_books=rated_books,
            reviewed_books=reviewed_books,
            followers=user.followers,
            following=user.following,
        )


class UserPublic(UserMini):
    is_author: bool
    shelves: List[ShelfMini] = []
    rated_books: List[RatedBook] = []
    reviewed_books: List[ReviewedBook] = []
    followers: List[UserMini] = []
    following: List[UserMini] = []
    is_following: Optional[bool] = None

    @classmethod
    def from_user(cls, user: User, auth_user_id: int):
        is_following = any(follower.id == auth_user_id for follower in user.followers)
        rated_books = list(map(RatedBook.from_rating, user.rated_books))
        reviewed_books = list(map(ReviewedBook.from_review, user.reviewed_books))

        return cls(
            id=user.id,
            is_author=user.is_author,
            name=user.name,
            last_name=user.last_name,
            shelves=user.shelves,
            rated_books=rated_books,
            reviewed_books=reviewed_books,
            followers=user.followers,
            following=user.following,
            is_following=is_following,
        )
