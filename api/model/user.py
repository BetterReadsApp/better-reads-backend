from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .review import Review
from .shelf import Shelf, ShelfForm
from .rating import Rating
from .following import Following


class UserBase(SQLModel):
    name: str = "John"
    last_name: str = "Doe"
    email: str = "example@email.com"


class UserFormRegister(UserBase):
    password: str = "s0mepassw0rd"


class UserFormLogin(SQLModel):
    email: str = "example@email.com"
    password: str = "s0mepassw0rd"


class User(UserFormRegister, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    shelves: List[Shelf] = Relationship(back_populates="user")
    rated_books: List[Rating] = Relationship(back_populates="user")
    reviewed_books: List[Review] = Relationship(back_populates="user")
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


class UserTiny(SQLModel):
    id: int
    name: str
    last_name: str


class UserPrivate(UserBase):
    id: int
    shelves: List[ShelfForm] = []
    rated_books: List[Rating] = []
    reviewed_books: List[Review] = []
    followers: List[UserTiny] = []
    following: List[UserTiny] = []


class UserPublic(UserTiny):
    shelves: List[ShelfForm] = []
    rated_books: List[Rating] = []
    reviewed_books: List[Review] = []
    followers: List[UserTiny] = []
    following: List[UserTiny] = []
    is_following: Optional[bool] = None

    @classmethod
    def from_private(cls, user: UserPrivate, auth_user_id: int):
        is_following = any(follower.id == auth_user_id for follower in user.followers)

        return cls(
            id=user.id,
            name=user.name,
            last_name=user.last_name,
            shelves=user.shelves,
            rated_books=user.rated_books,
            reviewed_books=user.reviewed_books,
            followers=user.followers,
            following=user.following,
            is_following=is_following,
        )
