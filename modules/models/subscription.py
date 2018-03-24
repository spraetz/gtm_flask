import account
from base import BaseModel
from database import db
from enum import Enum
import datetime


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
    converted_date = db.Column(db.Date)
    conversion_emails_sent = db.Column(db.Integer, nullable=True)

    # Phone alerts
    text_alerts = db.Column(db.Boolean, default=True)
    voice_alerts = db.Column(db.Boolean, default=False)
    voice_alerts_phone = db.Column(db.String(64), default="home_phone")  # Either "home_phone" or "mobile_phone"

    MINIMUM_SUBSCRIPTION_LENGTH_DAYS = 30

    def is_overdue(self):
        return self.end_date < datetime.date.today()

    def get_account(self):
        return account.Account.query.filter_by(id=self.account_id).first()

    def start_subscription(self):
        self.status = SubscriptionStatuses.active
        self.type = SubscriptionTypes.paid
        self.start_date = datetime.date.today()
        self.end_date = datetime.date.today() + datetime.timedelta(days=365)

        # TODO: Add to MailChimp
        self.save()

    def expire_subscription(self):
        self.status = SubscriptionStatuses.expired

        # TODO: Remove from MailChimp
        self.save()

    def convert_subscription(self):
        self.status = SubscriptionStatuses.converted
        self.save()

        # TODO: Make sure you can't double add someone to MailChimp
        new_sub = Subscription(status=SubscriptionStatuses.active,
                               type=SubscriptionTypes.paid,
                               account_id=self.account_id)
        new_sub.save()
        new_sub.start_subscription()
