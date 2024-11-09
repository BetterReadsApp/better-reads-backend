"""modificar_columna_publication_date_de_books

Revision ID: 8b7b76f103dc
Revises: fa9dc78ff115
Create Date: 2024-11-09 12:32:52.025375

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8b7b76f103dc"
down_revision: Union[str, None] = "fa9dc78ff115"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "books",
        "publication_date",
        type_=sa.Date,
        postgresql_using="publication_date::date",
    )


def downgrade() -> None:
    op.alter_column(
        "books",
        "publication_date",
        type_=sa.DateTime,
        postgresql_using="publication_date::timestamp",
    )
