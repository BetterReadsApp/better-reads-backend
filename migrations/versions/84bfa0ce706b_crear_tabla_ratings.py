"""crear_tabla_ratings

Revision ID: 84bfa0ce706b
Revises: 003dc0e8dbb7
Create Date: 2024-10-26 22:55:35.132733

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "84bfa0ce706b"
down_revision: Union[str, None] = "003dc0e8dbb7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ratings",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), primary_key=True),
        sa.Column("value", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ratings")
