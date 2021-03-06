"""empty message

Revision ID: 575d95a9a629
Revises: c60b68f2dbd8
Create Date: 2018-02-17 10:25:56.292585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '575d95a9a629'
down_revision = 'c60b68f2dbd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('str', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('int', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'test_pkey')
    )
    # ### end Alembic commands ###
