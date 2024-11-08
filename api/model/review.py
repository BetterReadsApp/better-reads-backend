from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .enums.book_genre import BookGenre


class ReviewForm(SQLModel):
    review: str = Field(default="", min_length=10, max_length=500)


class Review(ReviewForm, table=True):
    _tablename_ = "reviews"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    book_id: Optional[int] = Field(
        default=None, foreign_key="books.id", primary_key=True
    )

    user: "User" = Relationship(back_populates="reviewed_books")
    book: "Book" = Relationship(back_populates="reviews")


class ReviewedBook(SQLModel):
    book_id: int
    title: str
    author: str
    genre: BookGenre
    review: str

    @classmethod
    def from_review(cls, review: Review):
        return cls(
            book_id=review.book.id,
            review=review.review,
            title=review.book.title,
            author=review.book.author,
            genre=review.book.genre,
        )


class ReviewerUser(SQLModel):
    user_id: int
    name: str
    last_name: str
    review: str

    @classmethod
    def from_review(cls, review: Review):
        return cls(
            user_id=review.user.id,
            name=review.user.name,
            last_name=review.user.last_name,
            review=review.review,
        )
