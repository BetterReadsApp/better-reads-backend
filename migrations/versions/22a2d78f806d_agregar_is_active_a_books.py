"""Agregar is_active a books

Revision ID: 22a2d78f806d
Revises: bd3a90fb6aa6
Create Date: 2024-11-18 11:58:02.064874

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "22a2d78f806d"
down_revision: Union[str, None] = "bd3a90fb6aa6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "books",
        sa.Column(
            "is_active",
            sa.Boolean,
            nullable=False,
            server_default="true",
        ),
    )


def downgrade() -> None:
    op.drop_column("books", "is_active")
