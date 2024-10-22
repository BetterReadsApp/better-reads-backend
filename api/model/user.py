from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str
    password: str


class UserForm(UserBase):
    name: str
    last_name: str


class User(UserForm, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    # name: Optional[str] = Field(default=None)
    # last_name: Optional[str] = Field(default=None)
