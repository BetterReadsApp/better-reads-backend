from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .rating import Rating


class BookForm(SQLModel):
    title: str
    summary: str
    author: str
    pages: int
    publication_date: datetime


class Book(BookForm, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)
    average_rating: Optional[float] = Field(default=None)
    ratings: List[Rating] = Relationship(back_populates="book")


class BookPublic(BookForm):
    id: int
    average_rating: Optional[float]
    ratings: List[Rating] = []
    your_rating: Optional[int] = None

    def load_rating_by(self, user):
        self.your_rating = next(
            (rating.value for rating in self.ratings if rating.user == user)
        )
