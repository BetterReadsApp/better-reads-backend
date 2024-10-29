from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .shelf import Shelf, ShelfForm
from .rating import Rating
""" from .following import Following """


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
"""     following: List[Following] = Relationship(back_populates="follower") """


class UserPrivate(UserBase):
    id: int
    shelves: List[ShelfForm] = []
    rated_books: List[Rating] = []


class UserPublic(UserBase):
    id: int
