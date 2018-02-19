from database import db
from base import BaseModel


class Account(BaseModel, db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
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

    def __repr__(self):
        return "<Account object: id={} email={}>".format(self.id, self.email)
