from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class RatingForm(SQLModel):
    value: int


class Rating(SQLModel, table=True):
    __tablename__ = "ratings"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    book_id: Optional[int] = Field(
        default=None, foreign_key="books.id", primary_key=True
    )
    value: int = 1

    user: "User" = Relationship(back_populates="rated_books")
    book: "Book" = Relationship(back_populates="ratings")

    def update_average(self, times_rated):
        average_rating = self.book.average_rating if self.book.average_rating else 0
        self.book.average_rating = (average_rating * times_rated + self.value) / (
            times_rated + 1
        )
