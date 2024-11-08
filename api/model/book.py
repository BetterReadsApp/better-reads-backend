from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .review import Review, ReviewerUser
from .book_shelf_link import BookShelfLink
from .rating import RaterUser
from .enums.book_genre import BookGenre


class BookToShelfForm(SQLModel):
    book_id: int


class BookForm(SQLModel):
    title: str
    summary: str
    genre: BookGenre
    author: str
    pages: int
    publication_date: datetime


class Book(BookForm, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)
    average_rating: Optional[float] = Field(default=None)
    ratings: List["Rating"] = Relationship(back_populates="book")
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
    ratings: List[RaterUser] = []
    reviews: List[ReviewerUser] = []

    @classmethod
    def from_book(cls, book):
        ratings = list(map(RaterUser.from_rating, book.ratings))
        reviews = list(map(ReviewerUser.from_review, book.reviews))

        return cls(
            id=book.id,
            title=book.title,
            summary=book.summary,
            genre=book.genre,
            author=book.author,
            pages=book.pages,
            publication_date=book.publication_date,
            average_rating=book.average_rating,
            ratings=ratings,
            reviews=reviews,
        )

    def load_info_for(self, user):
        self.load_rating_for(user)
        self.load_review_for(user)

    def load_rating_for(self, user):
        self.your_rating = next(
            (
                rater_user.value
                for rater_user in self.ratings
                if rater_user.user_id == user.id
            ),
            None,
        )

    def load_review_for(self, user):
        self.your_review = next(
            (
                reviewer_user.review
                for reviewer_user in self.reviews
                if reviewer_user.user_id == user.id
            ),
            None,
        )


class BookPublic(BookForm):
    id: int
    average_rating: Optional[float]
    ratings: List[RaterUser] = []
    reviews: List[ReviewerUser] = []

    @classmethod
    def from_book(cls, book):
        ratings = list(map(RaterUser.from_rating, book.ratings))
        reviews = list(map(ReviewerUser.from_review, book.reviews))

        return cls(
            id=book.id,
            title=book.title,
            summary=book.summary,
            genre=book.genre,
            author=book.author,
            pages=book.pages,
            publication_date=book.publication_date,
            average_rating=book.average_rating,
            ratings=ratings,
            reviews=reviews,
        )


class BookAndShelfForm(SQLModel):
    book_id: int
    user_id: int
    name: str


class BookMini(SQLModel):
    id: int
    title: str
    author: str
    genre: BookGenre
