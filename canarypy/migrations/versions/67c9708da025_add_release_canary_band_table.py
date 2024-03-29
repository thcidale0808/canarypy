"""add release canary band table.

Revision ID: 67c9708da025
Revises: 33873c5a7bbe
Create Date: 2023-05-13 15:40:29.225959
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "67c9708da025"
down_revision = "33873c5a7bbe"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "release_canary_band",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("release_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["release_id"],
            ["release.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "signal",
        sa.Column(
            "release_canary_band_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
    )
    op.create_foreign_key(
        None, "signal", "release_canary_band", ["release_canary_band_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "signal", type_="foreignkey")
    op.drop_column("signal", "release_canary_band_id")
    op.drop_table("release_canary_band")
    # ### end Alembic commands ###
