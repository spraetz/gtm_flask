from database import db


class BaseModel(object):
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
