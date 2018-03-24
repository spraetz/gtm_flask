from sqlalchemy.orm.attributes import InstrumentedAttribute

from base import BaseModel
from database import db
from subscription import Subscription


class Account(BaseModel):
    __tablename__ = "accounts"

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(255), unique=True)

    # Phone Fields
    home_phone = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(10))

    # Address Fields
    street_address = db.Column(db.String(255))
    secondary_address = db.Column(db.String(255))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))

    # Info fields
    default_subscription_price = db.Column(db.Integer())

    def __repr__(self):
        return "<Account object: id={} email={}>".format(self.id, self.email)

    @classmethod
    def get_fields(cls):
        return [attr for attr in dir(Account) if isinstance(getattr(Account, attr), InstrumentedAttribute)]

    def get_field_values(self):
        return [getattr(self, field) for field in self.get_fields()]

    def get_subscriptions(self):
        return Subscription.query.filter_by(account_id=self.id).all()
