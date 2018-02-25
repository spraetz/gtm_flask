from database import db


class BaseModel(db.Model):
    # This is required to make this a real base class:
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#abstract
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_id(cls, id_to_search_for):
        return cls.query.filter_by(id=id_to_search_for).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def refresh(self):
        db.session.refresh(self)
