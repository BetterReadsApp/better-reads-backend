from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Review(SQLModel, table=True):
    _tablename_ = "reviews"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    book_id: Optional[int] = Field(
        default=None, foreign_key="books.id", primary_key=True
    )
    review: str = Field(default="", min_length=1, max_length=500)

    user: "User" = Relationship(back_populates="reviewed_books")
    book: "Book" = Relationship(back_populates="reviews")