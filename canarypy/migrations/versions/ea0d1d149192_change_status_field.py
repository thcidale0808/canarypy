"""change status field.

Revision ID: ea0d1d149192
Revises: 4a95c3cf7adc
Create Date: 2023-04-22 16:05:23.603570
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ea0d1d149192"
down_revision = "4a95c3cf7adc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "signal",
        "status",
        existing_type=sa.BOOLEAN(),
        type_=sa.String(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "signal",
        "status",
        existing_type=sa.String(),
        type_=sa.BOOLEAN(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
