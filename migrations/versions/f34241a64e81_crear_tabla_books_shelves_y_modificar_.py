"""crear_tabla_books_shelves_y_modificar_columna_name

Revision ID: f34241a64e81
Revises: 8a28ac8cd89f
Create Date: 2024-11-02 14:50:36.256869

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f34241a64e81"
down_revision: Union[str, None] = "8a28ac8cd89f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("shelves", sa.Column("id", sa.Integer, sa.Identity(), nullable=False))
    op.execute(
        "UPDATE shelves SET id = nextval(pg_get_serial_sequence('shelves', 'id')) WHERE id IS NULL;"
    )
    op.drop_constraint("pk_shelves", "shelves", type_="primary")
    op.create_primary_key("pk_shelves", "shelves", ["id"])

    op.create_table(
        "books_shelves",
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), primary_key=True),
        sa.Column(
            "shelf_id",
            sa.Integer,
            sa.ForeignKey("shelves.id"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_constraint("pk_shelves", "shelves", type_="primary")
    op.create_primary_key("pk_shelves", "shelves", ["name", "user_id"])
    op.drop_column("shelves", "id")

    op.drop_table("books_shelves")
