from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .shelf import Shelf, ShelfForm
from .rating import Rating
from .following import Following


class UserBase(SQLModel):
    name: str
    last_name: str
    email: str


class UserFormRegister(UserBase):
    password: str


class UserFormLogin(SQLModel):
    email: str
    password: str


class User(UserFormRegister, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    shelves: List[Shelf] = Relationship(back_populates="user")
    rated_books: List[Rating] = Relationship(back_populates="user")
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


class UserTiny(UserBase):
    id: int


class UserPublic(UserBase):
    id: int
    shelves: List[ShelfForm] = []
    rated_books: List[Rating] = []
    followers: List[UserTiny] = []
    following: List[UserTiny] = []
