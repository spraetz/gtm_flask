from tests.base_test import BaseTest


class TestSubscriptions(BaseTest):
    def test_account_foreign_key(self):
        account = self.create_account()
        subscription = self.create_subscription(account)
        subscription.refresh()
        self.assertEqual(subscription.account_id, account.id)

    def test_get_account(self):
        account = self.create_account()
        subscription = self.create_subscription(account)

        account_to_assert = subscription.get_account()
        self.assertEqual(account.email, account_to_assert.email)

    def test_date_format(self):
        account = self.create_account()
        subscription = self.create_subscription(account)

        subscription.start_date = "2018-01-01"
        subscription.save()
