import account
from base import BaseModel
from database import db


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)

    def get_account(self):
        return account.Account.query.filter_by(id=self.account_id).first()
