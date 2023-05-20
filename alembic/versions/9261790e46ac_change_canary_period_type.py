"""change canary period type

Revision ID: 9261790e46ac
Revises: 1c26034449b9
Create Date: 2023-05-20 06:01:28.735292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9261790e46ac'
down_revision = '1c26034449b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('release', 'canary_period',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('release', 'canary_period',
               existing_type=sa.Numeric(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
