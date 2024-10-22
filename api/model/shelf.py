from typing import Optional
from sqlmodel import SQLModel, Field


class ShelfForm(SQLModel):
    name: str
    user_id: int = Field(default=None, foreign_key="users.id")


class Shelf(ShelfForm, table=True):
    __tablename__ = "shelves"

    id: Optional[int] = Field(default=None, primary_key=True)
