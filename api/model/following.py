from sqlmodel import SQLModel, Field
from typing import Optional


class Following(SQLModel, table=True):
    __tablename__ = "followings"

    follower_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    following_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
