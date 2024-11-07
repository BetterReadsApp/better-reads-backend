"""crear_tablas_iniciales

Revision ID: fa9dc78ff115
Revises:
Create Date: 2024-10-21 14:32:35.264584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fa9dc78ff115"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("password", sa.String(200), nullable=False),
    )
    op.create_table(
        "followings",
        sa.Column(
            "follower_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True
        ),
        sa.Column(
            "following_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True
        ),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("summary", sa.String(200), nullable=False),
        sa.Column("genre", sa.String(50), nullable=False),
        sa.Column("author", sa.String(50), nullable=False),
        sa.Column("pages", sa.Integer, nullable=False),
        sa.Column("publication_date", sa.DateTime, nullable=False),
        sa.Column("average_rating", sa.Float, nullable=True),
    )
    op.create_table(
        "shelves",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_table(
        "books_shelves",
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), primary_key=True),
        sa.Column(
            "shelf_id", sa.Integer, sa.ForeignKey("shelves.id"), primary_key=True
        ),
    )
    op.create_table(
        "ratings",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), primary_key=True),
        sa.Column("value", sa.Integer, nullable=False),
    )
    op.create_table(
        "reviews",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), primary_key=True),
        sa.Column("review", sa.String(200), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("followings")
    op.drop_table("books")
    op.drop_table("shelves")
    op.drop_table("books_shelves")
    op.drop_table("ratings")
    op.drop_table("reviews")
