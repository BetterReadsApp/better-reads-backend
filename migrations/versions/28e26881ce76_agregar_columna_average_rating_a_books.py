"""agregar_columna_average_rating_a_books

Revision ID: 28e26881ce76
Revises: 84bfa0ce706b
Create Date: 2024-10-26 23:50:12.107416

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "28e26881ce76"
down_revision: Union[str, None] = "84bfa0ce706b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "books",
        sa.Column(
            "average_rating",
            sa.Float,
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("books", "average_rating")
