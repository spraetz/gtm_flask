from base import BaseModel
from database import db


class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    # TODO: security is a thing
    password = db.Column(db.String())

    def __repr__(self):
        return "<User object: id={} email={}>".format(self.id, self.email)

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id).decode('utf8')

    @classmethod
    def create_user(cls, email, password):
        user = User(email=email, password=password)
        user.save()
