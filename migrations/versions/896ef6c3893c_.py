"""empty message

Revision ID: 896ef6c3893c
Revises: df19e4d88243
Create Date: 2018-02-19 16:51:59.739574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '896ef6c3893c'
down_revision = 'df19e4d88243'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###