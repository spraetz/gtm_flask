from __future__ import print_function

from flask import url_for
from flask_testing import TestCase

from modules.models.account import Account
from modules.models.subscription import Subscription, SubscriptionTypes, SubscriptionStatuses
from modules.models.user import User
from run import db, create_app


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
        user = User()
        user.email = email
        user.password = password
        user.save()
        return user

    @staticmethod
    def create_account(email="bob@aol.com"):
        account = Account()
        account.email = email
        account.default_subscription_price = 12500
        account.first_name = "Bob"
        account.last_name = "Aol.com"
        account.save()
        return account

    @staticmethod
    def create_subscription(account, sub_type=SubscriptionTypes.trial, status=SubscriptionStatuses.active,
                            end_date="2019-01-01"):

        subscription = Subscription(account_id=account.id,
                                    type=sub_type,
                                    status=status,
                                    start_date="2018-01-01",
                                    end_date=end_date)
        subscription.save()
        return subscription

    def login_user(self, user):
        # Login the user (and make sure it was successful)
        form_data = {
            "email": user.email,
            "password": user.password
        }

        self.assert_redirects(self.client.post(url_for("public_blueprint.do_login"), data=form_data),
                              url_for("app_blueprint.show_home"))

    def logout_user(self):
        self.assert_redirects(self.client.get(url_for("public_blueprint.do_logout")),
                              url_for("public_blueprint.show_login"))
        response = self.client.get(url_for("app_blueprint.show_home"))
        self.assert_401(response, response.data)
