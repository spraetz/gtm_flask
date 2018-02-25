from tests.base_test import BaseTest


class TestAccounts(BaseTest):
    def test_get_subscriptions(self):
        account = self.create_account()
        self.create_subscription(account)
        self.create_subscription(account)
        other_account = self.create_account("other@account.biz")
        self.create_subscription(other_account)

        subscriptions = account.get_subscriptions()
        self.assertEqual(len(subscriptions), 2)
