from typing import Optional
from sqlmodel import SQLModel, Field


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


class UserPublic(UserBase):
    id: int
