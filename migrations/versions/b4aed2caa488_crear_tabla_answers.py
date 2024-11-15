"""crear_tabla_answers

Revision ID: b4aed2caa488
Revises: dcea9dd72e02
Create Date: 2024-11-15 12:36:04.333414

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4aed2caa488"
down_revision: Union[str, None] = "dcea9dd72e02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "question_id", sa.Integer, sa.ForeignKey("questions.id"), nullable=False
        ),
        sa.Column("selected_choice", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("answers")
