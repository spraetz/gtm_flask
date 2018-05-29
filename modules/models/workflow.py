from base import BaseModel
from database import db
from enum import Enum
import datetime

from subscription import Subscription


class Workflow(BaseModel):
    __abstract__ = True

    status = db.Column(db.Integer, nullable=False)

    @staticmethod
    def days_later(days):
        return datetime.date.today() + datetime.timedelta(days=days)


class ConversionWorkflowStatus(Enum):
    ok = 2000
    sent_four_week_notice = 28
    sent_two_week_notice = 14
    sent_one_week_notice = 7
    sent_final_notice = 0


class ConversionWorkflow(Workflow):
    __tablename__ = "conversion_workflows"

    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)

    def get_subscription(self):
        return Subscription.get_by_id(self.subscription_id)

    @classmethod
    def get_items_due_today(cls):
        return ConversionWorkflow.query.join(Subscription).filter(Subscription.id == ConversionWorkflow.id). \
            filter(Subscription.end_date <= cls.days_later(0)). \
            filter(ConversionWorkflow.status == ConversionWorkflowStatus.sent_one_week_notice). \
            all()


class RenewalWorkflowStatus(Enum):
    ok = 0
    four_week_notification = 100
    two_week_notification = 200
    one_week_notification = 300
    due_date_notification = 400


class RenewalWorkflow(Workflow):
    __tablename__ = "renewal_workflows"

    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)
