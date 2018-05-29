from freezegun import freeze_time

from lib.jobs import DailyCron
from tests.base_test import BaseTest


class DailyJobBaseTest(BaseTest):

    def setUp(self):
        super(DailyJobBaseTest, self).setUp()
        self.account = self.create_account()


@freeze_time("2019-01-01")
class TestDailyJob(DailyJobBaseTest):

    def test_job_init_method(self):
        dc = DailyCron()
        self.assertEqual(len(dc.notify_subscriptions_due_today.workflow_states), 0)
