from app import db


class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    str = db.Column(db.String())
    int = db.Column(db.Integer)

    def __repr__(self):
        return '<id {}>'.format(self.id)
