from modules.models.database import db
from modules.models.user import User
from tests.base_test import BaseTest


class TestShowIndex(BaseTest):
    def test_page_loads(self):
        self.assert_200(self.client.get("/"))


class TestShowLogin(BaseTest):
    def test_page_loads(self):
        self.assert_200(self.client.get("/login"))


class TestDoLogin(BaseTest):
    def setUp(self):
        super(TestDoLogin, self).setUp()
        user = User(email="admin@gtmarketing.com", password="123456")
        db.session.add(user)
        db.session.commit()
        self.user = user

    def test_success(self):
        form_data = {
            "email": self.user.email,
            "password": self.user.password,
        }
        resp = self.client.post("/login", data=form_data, follow_redirects=False)
        self.assert_redirects(resp, "/app/", resp.data)

    def test_wrong_password(self):
        form_data = {
            "email": self.user.email,
            "password": "not the right one"
        }
        self.assert_400(self.client.post("/login", data=form_data))

    def test_wrong_email(self):
        form_data = {
            "email": "fake@fake.fake",
            "password": "123456"
        }
        self.assert_400(self.client.post("/login", data=form_data))


class TestDoBootstrap(BaseTest):

    def test_success(self):
        self.assert_200(self.client.get("/bootstrap"))

    def test_already_done(self):
        self.test_success()
        self.assert_404(self.client.get("/bootstrap"))
