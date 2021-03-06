"""empty message

Revision ID: 6e2e33c416a5
Revises: 2244968dd320
Create Date: 2018-03-03 15:40:40.710333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e2e33c416a5'
down_revision = '2244968dd320'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('conversion_emails_sent', sa.Integer(), nullable=True))
    op.add_column('subscriptions', sa.Column('subscription_end_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('subscription_start_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('trial_end_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('trial_expired_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('trial_start_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriptions', 'trial_start_date')
    op.drop_column('subscriptions', 'trial_expired_date')
    op.drop_column('subscriptions', 'trial_end_date')
    op.drop_column('subscriptions', 'subscription_start_date')
    op.drop_column('subscriptions', 'subscription_end_date')
    op.drop_column('subscriptions', 'conversion_emails_sent')
    # ### end Alembic commands ###
