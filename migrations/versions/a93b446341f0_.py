"""empty message

Revision ID: a93b446341f0
Revises: 5f40679c0d17
Create Date: 2018-03-10 16:11:40.949388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a93b446341f0'
down_revision = '5f40679c0d17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('wtf', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriptions', 'wtf')
    # ### end Alembic commands ###