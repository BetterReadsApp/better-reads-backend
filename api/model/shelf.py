from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .book_shelf_link import BookShelfLink
from .book import Book


class ShelfForm(SQLModel):
    name: str


class Shelf(ShelfForm, table=True):
    __tablename__ = "shelves"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="shelves")
    books: List[Book] = Relationship(back_populates="shelves", link_model=BookShelfLink)

    def add(self, book):
        self.books.append(book)

    def contains(self, book):
        return book in self.books


class ShelfPublic(SQLModel):
    id: int
    name: str
    user_id: int


class ShelfPrivate(SQLModel):
    id: int
    name: str
    user_id: int
    books: List[Book]
