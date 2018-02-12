from __future__ import print_function
from flask_testing import TestCase

from run import db, create_app
from modules.models.user import User


class BaseTest(TestCase):

    def create_app(self):

        app = create_app()
        db.init_app(app)

        if not app.config.get("TESTING"):
            raise Exception("Cannot run tests unless in test mode")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def create_user(email="admin@gtmarketing.com", password="123456"):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def login_user(self, user):
        # Login the user (and make sure it was successful)
        form_data = {
            "email": user.email,
            "password": user.password
        }

        self.assert_redirects(self.client.post("/login", data=form_data), "/app")

    def logout_user(self):
        self.assert_redirects(self.client.get("/logout"), "/login")
        self.assert_401(self.client.get("app"))
