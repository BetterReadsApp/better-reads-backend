"""eliminar_columna_id_en_shelves

Revision ID: 003dc0e8dbb7
Revises: fa9dc78ff115
Create Date: 2024-10-26 19:44:23.917435

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "003dc0e8dbb7"
down_revision: Union[str, None] = "fa9dc78ff115"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("shelves", "id")
    op.create_primary_key("pk_shelves", "shelves", ["name", "user_id"])


def downgrade() -> None:
    op.add_column(
        "shelves",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
        ),
    )
    op.drop_constraint("pk_shelves", "shelves")
