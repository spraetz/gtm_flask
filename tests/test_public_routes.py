from flask import url_for

from modules.models.database import db
from modules.models.user import User
from tests.base_test import BaseTest


class TestShowIndex(BaseTest):
    def test_page_loads(self):
        self.assert_200(self.client.get("/"))


class TestShowLogin(BaseTest):
    def test_page_loads(self):
        self.assert_200(self.client.get(url_for("public_blueprint.show_login")))


class TestDoLogin(BaseTest):
    def setUp(self):
        super(TestDoLogin, self).setUp()
        user = User()
        user.email = "admin@gtmarketing.com"
        user.password = "123456"
        user.save()
        self.user = user

    def test_success(self):
        form_data = {
            "email": self.user.email,
            "password": self.user.password,
        }
        resp = self.client.post(url_for("public_blueprint.do_login"), data=form_data, follow_redirects=False)
        self.assert_redirects(resp, url_for("app_blueprint.show_home"), resp.data)

    def test_wrong_password(self):
        form_data = {
            "email": self.user.email,
            "password": "not the right one"
        }
        self.assert_400(self.client.post(url_for("public_blueprint.do_login"), data=form_data))

    def test_wrong_email(self):
        form_data = {
            "email": "fake@fake.fake",
            "password": "123456"
        }
        self.assert_400(self.client.post(url_for("public_blueprint.do_login"), data=form_data))


class TestDoBootstrap(BaseTest):

    def test_success(self):
        self.assert_200(self.client.get(url_for("public_blueprint.do_bootstrap_database")))

    def test_already_done(self):
        self.test_success()
        self.assert_404(self.client.get(url_for("public_blueprint.do_bootstrap_database")))
