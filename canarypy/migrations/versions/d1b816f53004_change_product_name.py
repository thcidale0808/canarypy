"""change product name.

Revision ID: d1b816f53004
Revises: 738957fcc3bc
Create Date: 2023-05-03 20:34:52.882065
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d1b816f53004"
down_revision = "738957fcc3bc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product", sa.Column("name", sa.String(), nullable=True))
    op.create_index("idx_product_name", "product", ["name"], unique=True)
    op.create_unique_constraint(None, "product", ["name"])
    op.drop_column("product", "description")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product",
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "product", type_="unique")
    op.drop_index("idx_product_name", table_name="product")
    op.drop_column("product", "name")
    # ### end Alembic commands ###
