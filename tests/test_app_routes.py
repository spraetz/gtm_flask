from tests.base_test import BaseTest


class AppTest(BaseTest):
    def setUp(self):
        super(AppTest, self).setUp()

        # Create a user
        self.user = self.create_user()

        self.login_user(self.user)


class TestShowApp(AppTest):
    def test_page_loads(self):
        self.assert_200(self.client.get("/app"))

    def test_login_required(self):
        self.logout_user()
        self.assert_401(self.client.get("/app"))
