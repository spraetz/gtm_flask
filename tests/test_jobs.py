from tests.base_test import BaseTest
from freezegun import freeze_time
from lib.jobs import DailyCron


class DailyJobBaseTest(BaseTest):

    def setUp(self):
        super(DailyJobBaseTest, self).setUp()
        self.account = self.create_account()


@freeze_time("2019-01-01")
class TestDailyJob(DailyJobBaseTest):

    def test_get_subscriptions_due_in_28_days(self):

        # Create subscription with end_date 28 days from now.
        subscription = self.create_subscription(self.account, end_date=DailyCron.days_later(28))

        dc = DailyCron()

        self.assertEqual(dc.subscriptions[0].id, subscription.id)
        self.assertEqual(len(dc.subscriptions), 1)

    def test_get_subscriptions_due_in_14_days(self):

        # Create subscription with end_date 14 days from now.
        subscription = self.create_subscription(self.account, end_date=DailyCron.days_later(14))

        dc = DailyCron()

        self.assertEqual(dc.subscriptions[0].id, subscription.id)
        self.assertEqual(len(dc.subscriptions), 1)

    def test_get_subscriptions_due_in_7_days(self):

        # Create subscription with end_date 7 days from now.
        subscription = self.create_subscription(self.account, end_date=DailyCron.days_later(7))

        dc = DailyCron()

        self.assertEqual(dc.subscriptions[0].id, subscription.id)
        self.assertEqual(len(dc.subscriptions), 1)

    def test_get_subscriptions_due_in_today(self):

        # Create subscription with end_date today.
        subscription = self.create_subscription(self.account, end_date=DailyCron.days_later(0))

        dc = DailyCron()

        self.assertEqual(dc.subscriptions[0].id, subscription.id)
        self.assertEqual(len(dc.subscriptions), 1)

    def test_get_subscriptions_multiple_days(self):

        # Create subscription with end_date of today and 7 days from now.
        self.create_subscription(self.account, end_date=DailyCron.days_later(0))
        self.create_subscription(self.account, end_date=DailyCron.days_later(1))
        self.create_subscription(self.account, end_date=DailyCron.days_later(7))

        dc = DailyCron()

        self.assertEqual(len(dc.subscriptions), 2)