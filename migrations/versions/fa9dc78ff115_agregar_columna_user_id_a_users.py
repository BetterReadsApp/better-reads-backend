"""agregar_columna_user_id_a_users

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
    op.add_column(
        "shelves",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id"),
            nullable=False,
            server_default="1",
        ),
    )


def downgrade() -> None:
    op.drop_column("shelves", "user_id")
