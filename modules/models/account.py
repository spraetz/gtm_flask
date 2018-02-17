from database import db
from base import BaseModel


class Account(BaseModel, db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(255), unique=True)

    home_phone = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(10))

    def __repr__(self):
        return "<Account object: id={} email={}>".format(self.id, self.email)

    @classmethod
    def create_account(cls, email, first_name, last_name, home_phone, mobile_phone):
        account = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            home_phone=home_phone,
            mobile_phone=mobile_phone
        )
        account.save()
