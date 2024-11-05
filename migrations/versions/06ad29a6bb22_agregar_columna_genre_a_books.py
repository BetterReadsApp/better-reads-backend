"""agregar_columna_genre_a_books

Revision ID: 06ad29a6bb22
Revises: f34241a64e81
Create Date: 2024-11-05 21:06:56.804586

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "06ad29a6bb22"
down_revision: Union[str, None] = "f34241a64e81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "books",
        sa.Column(
            "genre",
            sa.String(50),
            nullable=False,
            server_default="THRILLER",
        ),
    )


def downgrade() -> None:
    op.drop_column("books", "genre")
