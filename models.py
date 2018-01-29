from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
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


class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    str = db.Column(db.String())
    int = db.Column(db.Integer)

    def __repr__(self):
        return '<id {}>'.format(self.id)
