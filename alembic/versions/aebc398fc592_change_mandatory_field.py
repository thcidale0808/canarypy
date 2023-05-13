"""change mandatory field

Revision ID: aebc398fc592
Revises: f19eb484f268
Create Date: 2023-05-13 15:51:09.967636

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aebc398fc592'
down_revision = '67c9708da025'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('signal', 'release_canary_band_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('signal', 'release_canary_band_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
