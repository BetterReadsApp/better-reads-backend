from sqlmodel import SQLModel, Field
from typing import Optional


class BookShelfLink(SQLModel, table=True):
    __tablename__ = "books_shelves"

    book_id: Optional[int] = Field(
        default=None, foreign_key="books.id", primary_key=True
    )
    shelf_id: Optional[int] = Field(
        default=None, foreign_key="shelves.id", primary_key=True
    )
