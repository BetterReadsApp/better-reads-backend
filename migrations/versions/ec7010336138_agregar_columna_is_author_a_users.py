"""agregar_columna_is_author_a_users

Revision ID: ec7010336138
Revises: 8b7b76f103dc
Create Date: 2024-11-11 13:34:55.356721

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ec7010336138"
down_revision: Union[str, None] = "8b7b76f103dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_author", sa.Boolean, nullable=False, server_default="false"),
    )


def downgrade() -> None:
    op.drop_column("users", "is_author")
