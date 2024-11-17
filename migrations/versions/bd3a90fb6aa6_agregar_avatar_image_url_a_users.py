"""Agregar avatar_image_url a users

Revision ID: bd3a90fb6aa6
Revises: b4aed2caa488
Create Date: 2024-11-17 11:27:20.541955

"""

from typing import Sequence, Union
from api.model.enums.avatar import Avatar

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd3a90fb6aa6"
down_revision: Union[str, None] = "b4aed2caa488"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "avatar_image_url",
            sa.String(300),
            nullable=False,
            server_default=Avatar.KIMBERLY.value,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "avatar_image_url")
