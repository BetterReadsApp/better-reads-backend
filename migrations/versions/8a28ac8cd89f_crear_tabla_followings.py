"""crear_tabla_followings

Revision ID: 8a28ac8cd89f
Revises: 28e26881ce76
Create Date: 2024-10-29 13:47:54.196315

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8a28ac8cd89f"
down_revision: Union[str, None] = "28e26881ce76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "followings",
        sa.Column(
            "follower_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True
        ),
        sa.Column(
            "following_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True
        ),
    )


def downgrade() -> None:
    op.drop_table("followings")
