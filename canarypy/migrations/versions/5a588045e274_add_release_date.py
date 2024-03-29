"""add release date.

Revision ID: 5a588045e274
Revises: ea0d1d149192
Create Date: 2023-04-22 18:57:49.724856
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5a588045e274"
down_revision = "ea0d1d149192"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("release", sa.Column("release_date", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("release", "release_date")
    # ### end Alembic commands ###
