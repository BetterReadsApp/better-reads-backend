from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from .review import Review
from .book_shelf_link import BookShelfLink
from .enums.book_genre import BookGenre


class BookToShelfForm(SQLModel):
    book_id: int


class BookForm(SQLModel):
    title: str
    summary: str
    genre: BookGenre
    pages: int
    publication_date: date
    cover_image_url: Optional[str]
    author_id: int = Field(default=None, foreign_key="users.id")


class Book(BookForm, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)
    average_rating: Optional[float] = Field(default=None)

    quizzes: List["Quiz"] = Relationship(back_populates="book")
    author: Optional["User"] = Relationship(back_populates="created_books")
    ratings: List["Rating"] = Relationship(back_populates="book")
    reviews: List[Review] = Relationship(back_populates="book")
    shelves: List["Shelf"] = Relationship(
        back_populates="books", link_model=BookShelfLink
    )

    def __eq__(self, other):
        return self.id == other.id


class BookAndShelfForm(SQLModel):
    book_id: int
    user_id: int
    name: str


class BookMini(SQLModel):
    id: int
    title: str
    author: Optional["UserMini"]
    genre: BookGenre
    publication_date: date
