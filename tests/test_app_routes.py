from flask import url_for

from modules.models.account import Account
from tests.base_test import BaseTest


class AppTest(BaseTest):
    def setUp(self):
        super(AppTest, self).setUp()

        # Create a user
        self.user = self.create_user()
        self.login_user(self.user)

        # Create some test data
        self.account = self.create_account()


class TestShowHome(AppTest):

    @staticmethod
    def get_url():
        return url_for("app_blueprint.show_home")

    def test_page_loads(self):
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_401(response, response.data)


class TestShowAccountList(AppTest):

    @staticmethod
    def get_url():
        return url_for("app_blueprint.show_accounts")

    def test_page_loads(self):
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_401(response, response.data)

    def test_account_shows(self):
        response = self.client.get(self.get_url(), follow_redirects=True)
        self.assertIn(self.account.email, response.data, "Could not find account in list.")


class TestShowAccount(AppTest):

    def get_url(self):
        return url_for("app_blueprint.show_account", account_id=self.account.id)

    def test_page_loads(self):
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_401(response, response.data)

    def test_delete_button_shows(self):
        response = self.client.get(self.get_url(), follow_redirects=True)
        self.assertIn(">Delete</button>", response.data, "Delete button missing")


class TestShowAccountCreate(AppTest):

    @staticmethod
    def get_url():
        return url_for("app_blueprint.show_create_account")

    def test_page_loads(self):
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_401(response, response.data)

    def test_delete_button_not_found(self):
        response = self.client.get(self.get_url(), follow_redirects=True)
        self.assertNotIn(">Delete</button>", response.data, "Delete button is present.")


class TestDoCreateAccount(AppTest):

    @staticmethod
    def get_url():
        return url_for("app_blueprint.do_create_account")

    def test_success(self):
        form_data = {
            "email": "test@data.biz",
            "first_name": "Foo",
            "last_name": "Bar",
            "home_phone": "0987654321",
            "mobile_phone": "0987654321"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=False)
        self.assert_redirects(response, url_for("app_blueprint.show_accounts"), response.data)

        account = Account.query.filter_by(email=form_data["email"]).first()
        self.assertIsNotNone(account)
        self.assertEquals(account.first_name, form_data["first_name"])

    def test_failure_no_email(self):
        form_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "home_phone": "0987654321",
            "mobile_phone": "0987654321"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=True)
        self.assert_400(response)
        self.assertIn("<label for=\"email\">Email</label>: This field is required.", response.data, response.data)

    def test_failure_duplicate_email(self):
        form_data = {
            "email": self.account.email,
            "first_name": "Foo",
            "last_name": "Bar",
            "home_phone": "0987654321",
            "mobile_phone": "0987654321"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=True)
        self.assert_400(response)
        self.assertIn("<label for=\"email\">Email</label>: Duplicate email detected.", response.data, response.data)


class TestDoSaveAccount(AppTest):

    def get_url(self):
        return url_for("app_blueprint.do_save_account", account_id=self.account.id)

    def test_success(self):

        form_data = {
            "id": self.account.id,
            "email": "test2@data.biz",
            "first_name": "Foo",
            "last_name": "Bar",
            "home_phone": "0987654321",
            "mobile_phone": "0987654321"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=False)
        self.assert_redirects(response, url_for("app_blueprint.show_accounts"), response.data)

        self.account.refresh()
        self.assertEquals(self.account.email, form_data["email"])

    def test_failure_duplicate_email(self):

        # Create a 2nd account
        second_account = self.create_account("second@account.biz")

        # Try to update the 1st account to have the same email as the second one.
        form_data = {
            "id": self.account.id,
            "email": second_account.email,
            "first_name": "Foo",
            "last_name": "Bar",
            "home_phone": "0987654321",
            "mobile_phone": "0987654321"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=False)
        self.assert_400(response)

        self.assertIn("<label for=\"email\">Email</label>: Duplicate email detected.", response.data, response.data)

    # TODO
    def test_failure_bad_phone_number(self):
        pass
