"""empty message

Revision ID: 099ad4b405c8
Revises: 
Create Date: 2018-01-28 16:24:45.398224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '099ad4b405c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('int', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'int')
    # ### end Alembic commands ###
