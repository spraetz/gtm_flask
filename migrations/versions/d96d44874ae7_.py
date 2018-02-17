"""empty message

Revision ID: d96d44874ae7
Revises: c5b13e22a037
Create Date: 2018-02-17 13:18:59.484284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd96d44874ae7'
down_revision = 'c5b13e22a037'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('first_name', sa.String(length=64), nullable=True))
    op.add_column('accounts', sa.Column('home_phone', sa.String(length=10), nullable=True))
    op.add_column('accounts', sa.Column('last_name', sa.String(length=64), nullable=True))
    op.add_column('accounts', sa.Column('mobile_phone', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'mobile_phone')
    op.drop_column('accounts', 'last_name')
    op.drop_column('accounts', 'home_phone')
    op.drop_column('accounts', 'first_name')
    # ### end Alembic commands ###
