from app import db


class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    str = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)


db.create_all()