from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .enums.book_genre import BookGenre


class RatingForm(SQLModel):
    value: int = 1


class Rating(RatingForm, table=True):
    __tablename__ = "ratings"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    book_id: Optional[int] = Field(
        default=None, foreign_key="books.id", primary_key=True
    )

    user: "User" = Relationship(back_populates="rated_books")
    book: "Book" = Relationship(back_populates="ratings")

    def update_average(self, times_rated):
        average_rating = self.book.average_rating if self.book.average_rating else 0
        self.book.average_rating = (average_rating * times_rated + self.value) / (
            times_rated + 1
        )


class RaterUser(SQLModel):
    user_id: int
    name: str
    last_name: str
    value: int

    @classmethod
    def from_rating(cls, rating: Rating):
        return cls(
            user_id=rating.user.id,
            name=rating.user.name,
            last_name=rating.user.last_name,
            value=rating.value,
        )


class RatedBook(SQLModel):
    book_id: int
    title: str
    author: str
    genre: BookGenre
    value: int

    @classmethod
    def from_rating(cls, rating: Rating):
        return cls(
            book_id=rating.book.id,
            value=rating.value,
            title=rating.book.title,
            author=rating.book.author,
            genre=rating.book.genre,
        )
