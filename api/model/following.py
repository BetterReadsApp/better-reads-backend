""" from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Following(SQLModel, table=True):
    __tablename__ = "followings"

    follower_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    following_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )

    follower: "User" = Relationship(back_populates="following")
    following: "User" = Relationship(back_populates="followers") """