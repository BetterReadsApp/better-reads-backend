from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .review import Review
from .rating import Rating
from .book_shelf_link import BookShelfLink
from enum import Enum


class Genre(Enum):
    THRILLER = "Thriller"
    HORROR = "Horror"
    HISTORY = "History"
    MANGA = "Manga"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    COMIC = "Comic"
    BIOGRAPHY = "Biography"
    FANTASY = "Fantasy"
    PHILOSOPHY = "Philosophy"


class BookToShelfForm(SQLModel):
    book_id: int


class BookForm(SQLModel):
    title: str
    summary: str
    genre: Genre
    author: str
    pages: int
    publication_date: datetime


class Book(BookForm, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)
    average_rating: Optional[float] = Field(default=None)
    ratings: List[Rating] = Relationship(back_populates="book")
    reviews: List[Review] = Relationship(back_populates="book")
    shelves: List["Shelf"] = Relationship(
        back_populates="books", link_model=BookShelfLink
    )

    def __eq__(self, other):
        return self.id == other.id


class BookPrivate(BookForm):
    id: int
    average_rating: Optional[float]
    your_rating: Optional[int] = None
    your_review: Optional[str] = None
    ratings: List[Rating] = []
    reviews: List[Review] = []

    def load_rating_by(self, user):
        self.your_rating = next(
            (rating.value for rating in self.ratings if rating.user == user), None
        )

    def load_review_by(self, user):
        self.your_review = next(
            (review.review for review in self.reviews if review.user == user), None
        )


class BookPublic(BookForm):
    id: int
    average_rating: Optional[float]
    ratings: List[Rating] = []
    reviews: List[Review] = []


class BookAndShelfForm(SQLModel):
    book_id: int
    user_id: int
    name: str


class BookMini(SQLModel):
    id: int
    title: str
    author: str
    genre: Genre
