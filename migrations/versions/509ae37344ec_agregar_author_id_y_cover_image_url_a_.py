"""agregar_author_id_y_cover_image_url_a_books

Revision ID: 509ae37344ec
Revises: ec7010336138
Create Date: 2024-11-12 13:32:06.270172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '509ae37344ec'
down_revision: Union[str, None] = 'ec7010336138'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("books", "author")
    op.add_column(
        "books",
        sa.Column(
            "author_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, server_default="1"
        ),
    )
    op.add_column(
        "books",
        sa.Column("cover_image_url", sa.String(300), nullable=True),
    )

def downgrade() -> None:
    op.add_column(
        "books",
        sa.Column("author", sa.String(50), nullable=False, server_default="Un autor"),
    )
    op.drop_column("books", "author_id")
    op.drop_column("books", "cover_image_url")