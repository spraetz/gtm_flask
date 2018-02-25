from modules.models.account import Account
from modules.models.subscription import Subscription
from tests.base_test import BaseTest


class TestSubscriptions(BaseTest):
    def test_account_foreign_key(self):
        account = Account(email="bob@aol.com")
        account.save()
        subscription = Subscription(account_id=account.id)
        subscription.save()
        subscription.refresh()
        self.assertEqual(subscription.account_id, account.id)

    def test_get_account(self):
        account = Account(email="bob@aol.com")
        account.save()
        subscription = Subscription(account_id=account.id)
        subscription.save()

        account_to_assert = subscription.get_account()
        self.assertEqual(account.email, account_to_assert.email)
