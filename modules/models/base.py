from database import db


class BaseModel(db.Model):
    # This is required to make this a real base class:
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#abstract
    __abstract__ = True

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
