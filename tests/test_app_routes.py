from tests.base_test import BaseTest


class AppTest(BaseTest):
    def setUp(self):
        super(AppTest, self).setUp()

        # Create a user
        self.user = self.create_user()

        self.login_user(self.user)


class TestShowHome(AppTest):

    url = "/app/"

    def test_page_loads(self):
        response = self.client.get(self.url, follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.url, follow_redirects=False)
        self.assert_401(response, response.data)


class TestShowAccounts(AppTest):
    url = "/accounts/"

    def test_page_loads(self):
        response = self.client.get(self.url, follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.url, follow_redirects=False)
        self.assert_401(response, response.data)


