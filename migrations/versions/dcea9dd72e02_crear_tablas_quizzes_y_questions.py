"""crear_tablas_quizzes_y_questions

Revision ID: dcea9dd72e02
Revises: 509ae37344ec
Create Date: 2024-11-12 22:24:53.650348

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dcea9dd72e02"
down_revision: Union[str, None] = "509ae37344ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quizzes",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
    )
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("quiz_id", sa.Integer, sa.ForeignKey("quizzes.id"), nullable=False),
        sa.Column("title", sa.String(150), nullable=False),
        sa.Column("choice_1", sa.String(150), nullable=False),
        sa.Column("choice_2", sa.String(150), nullable=False),
        sa.Column("choice_3", sa.String(150), nullable=False),
        sa.Column("choice_4", sa.String(150), nullable=False),
        sa.Column("correct_choice", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("quizzes")
    op.drop_table("questions")
