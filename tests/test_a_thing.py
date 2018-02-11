from tests.base_test import MyTest
from modules.models.user import User
from modules.models.database import db


class TestClass(MyTest):

    def test_something(self):

        assert not User.query.filter_by(email="spraetz@gmail.com").first()

        user = User(email="spraetz@gmail.com", password="123456")
        db.session.add(user)
        db.session.commit()
        assert User.query.filter_by(email="spraetz@gmail.com").first()
