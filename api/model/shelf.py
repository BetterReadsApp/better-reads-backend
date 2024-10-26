from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class ShelfForm(SQLModel):
    name: str = Field(primary_key=True)


class Shelf(ShelfForm, table=True):
    __tablename__ = "shelves"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    user: Optional["User"] = Relationship(back_populates="shelves")
