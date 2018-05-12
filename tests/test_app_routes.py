import datetime
from flask import url_for

from modules.models.account import Account
from tests.base_test import BaseTest
from modules.models.subscription import Subscription, SubscriptionStatuses, SubscriptionTypes


class AppTest(BaseTest):
    def setUp(self):
        super(AppTest, self).setUp()

        # Create a user
        self.user = self.create_user()
        self.login_user(self.user)

        # Create some test data
        self.account = self.create_account()
        self.subscription = self.create_subscription(self.account)


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


# TODO
class TestDoExportAccounts(AppTest):
    pass


class TestShowSubscription(AppTest):
    def get_url(self):
        return url_for("app_blueprint.show_subscription", account_id=self.account.id,
                       subscription_id=self.subscription.id)

    def test_page_loads(self):
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_401(response, response.data)


class TestShowCreateSubscription(AppTest):
    def get_url(self):
        return url_for("app_blueprint.show_create_subscription", account_id=self.account.id)

    def test_page_loads(self):
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_200(response, response.data)

    def test_login_required(self):
        self.logout_user()
        response = self.client.get(self.get_url(), follow_redirects=False)
        self.assert_401(response, response.data)


class TestDoCreateSubscription(AppTest):
    def get_url(self):
        return url_for("app_blueprint.do_create_subscription", account_id=self.account.id)

    def test_success(self):

        form_data = {
            "account_id": self.account.id,
            "type": SubscriptionTypes.paid,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "voice_alerts_phone": "home_phone"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=False)
        self.assert_redirects(response, url_for("app_blueprint.show_account", account_id=self.account.id),
                              response.data)

        # Find the created record
        self.assertEqual(len(self.account.get_subscriptions()), 2)

    def test_failure_start_date_after_end_date(self):

        form_data = {
            "account_id": self.account.id,
            "type": SubscriptionTypes.paid,
            "start_date": "2018-01-01",
            "end_date": "2017-01-01",  # Note the end date is a year before the start date
            "voice_alerts_phone": "home_phone"
        }

        response = self.client.post(self.get_url(), data=form_data)
        self.assert_400(response)
        self.assertIn("<label for=\"end_date\">End Date</label>: End Date must be after Start Date", response.data,
                      response.data)


class TestDoSaveSubscription(AppTest):
    def get_url(self):
        return url_for("app_blueprint.do_save_subscription", account_id=self.account.id,
                       subscription_id=self.subscription.id)

    def test_success(self):

        new_end_date = self.subscription.end_date + datetime.timedelta(days=365)

        form_data = {
            "id": self.subscription.id,
            "account_id": self.account.id,
            "type": SubscriptionTypes.paid,
            "status": SubscriptionStatuses.active,
            "start_date": "2018-01-01",
            "end_date": new_end_date,
            "voice_alerts_phone": "home_phone"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=False)
        self.assert_redirects(response, url_for("app_blueprint.show_account", account_id=self.account.id),
                              response.data)

        # Assert the record got modified
        self.subscription.refresh()
        self.assertEqual(self.subscription.end_date, new_end_date)

    def test_failure_subscription_too_short(self):

        new_end_date = self.subscription.start_date + datetime.timedelta(
            days=Subscription.MINIMUM_SUBSCRIPTION_LENGTH_DAYS - 1)

        form_data = {
            "id": self.subscription.id,
            "account_id": self.account.id,
            "type": SubscriptionTypes.paid,
            "status": SubscriptionStatuses.active,
            "start_date": "2018-01-01",
            "end_date": new_end_date,
            "voice_alerts_phone": "home_phone"
        }

        response = self.client.post(self.get_url(), data=form_data, follow_redirects=False)
        self.assert_400(response, response.data)
        self.assertIn("<label for=\"end_date\">End Date</label>: Subscriptions must be at least 30 days long.",
                      response.data, response.data)
