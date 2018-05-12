import account
from base import BaseModel
from database import db
from enum import Enum
import datetime
from lib.mailing_list import add_to_list, remove_from_list


class SubscriptionStatuses(Enum):
    active = "active"
    expired = "expired"
    converted = "converted"


class SubscriptionTypes(Enum):
    trial = "trial"
    paid = "paid"
    free = "free"


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    type = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    # Subscription properties
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    expired_date = db.Column(db.Date)

    # Phone alerts
    text_alerts = db.Column(db.Boolean, default=True)
    voice_alerts = db.Column(db.Boolean, default=False)
    voice_alerts_phone = db.Column(db.String(64), default="home_phone")  # Either "home_phone" or "mobile_phone"

    MINIMUM_SUBSCRIPTION_LENGTH_DAYS = 30

    def is_overdue(self):
        return self.end_date < datetime.date.today()

    def get_account(self):
        return account.Account.query.filter_by(id=self.account_id).first()

    def add_to_mailing_list(self):
        if self.status != SubscriptionStatuses.active:
            raise Exception("Cannot add a non-active subscription to mailing list.")
        add_to_list(self.get_account())

    def expire_subscription(self):
        self.status = SubscriptionStatuses.expired

        remove_from_list(self.get_account())
        self.save()

    def convert_subscription(self):
        self.status = SubscriptionStatuses.converted
        self.save()

        new_sub = Subscription(status=SubscriptionStatuses.active,
                               type=SubscriptionTypes.paid,
                               account_id=self.account_id,
                               start_date=self.end_date,
                               end_date=self.end_date + datetime.timedelta(days=365),
                               text_alerts=self.text_alerts,
                               voice_alerts=self.voice_alerts,
                               voice_alerts_phone=self.voice_alerts_phone)

        new_sub.save()
