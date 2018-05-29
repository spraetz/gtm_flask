from freezegun import freeze_time

from lib.utils import days_later
from modules.models.workflow import ConversionWorkflowStatus
from modules.workflow.subscription_conversion import NotifySubscriptionsDueToday
from tests.base_test import BaseTest


class DailyJobBaseTest(BaseTest):

    def setUp(self):
        super(DailyJobBaseTest, self).setUp()
        self.account = self.create_account()


@freeze_time("2019-01-01")
class TestDailyJob(DailyJobBaseTest):

    def test_subscriptions_due_today_process(self):
        # Create subscription with end_date 28 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(0))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_one_week_notice)

        process = NotifySubscriptionsDueToday()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_final_notice)
