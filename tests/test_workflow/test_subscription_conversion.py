from freezegun import freeze_time

from lib.utils import days_later
from modules.models.workflow import ConversionWorkflowStatus
from modules.workflow.subscription_conversion import NotifySubscriptionsDueToday, NotifySubscriptionsDueInSevenDays, \
    NotifySubscriptionsDueInFourteenDays, NotifySubscriptionsDueInTwentyEightDays
from tests.base_test import BaseTest


class ProcessBaseTest(BaseTest):

    def setUp(self):
        super(ProcessBaseTest, self).setUp()
        self.account = self.create_account()


@freeze_time("2019-01-01")
class TestConversionProcesses(ProcessBaseTest):

    # The happy path for subscriptions due today
    def test_subscriptions_due_today_process(self):
        # Create subscription with end_date 0 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(0))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_one_week_notice)

        process = NotifySubscriptionsDueToday()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_final_notice)

    # The job should find no subscriptions to process.
    def test_subscriptions_due_today_process_with_no_subscriptions_due(self):
        # Create subscription with end_date 1 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(1))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_one_week_notice)

        process = NotifySubscriptionsDueToday()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_one_week_notice)

    # If for whatever reason, the job fails to run for a day, it'll still pick up the overdue subscription.
    def test_subscriptions_due_today_with_overdue_subscription(self):
        # Create subscription with end_date 1 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(-1))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_one_week_notice)

        process = NotifySubscriptionsDueToday()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_final_notice)

    # Test multiple subscriptions at once.
    def test_multiple_subscriptions_due_today(self):
        # Create two subscriptions with end_date 0 days from now.
        subscription_one = self.create_subscription(self.account, end_date=days_later(0))
        workflow_state_one = self.create_conversion_workflow_state(subscription_one,
                                                                   ConversionWorkflowStatus.sent_one_week_notice)

        subscription_two = self.create_subscription(self.account, end_date=days_later(0))
        workflow_state_two = self.create_conversion_workflow_state(subscription_two,
                                                                   ConversionWorkflowStatus.sent_two_week_notice)

        process = NotifySubscriptionsDueToday()
        process.process()

        workflow_state_one.refresh()
        self.assertEqual(workflow_state_one.status, ConversionWorkflowStatus.sent_final_notice)

        workflow_state_two.refresh()
        self.assertEqual(workflow_state_two.status, ConversionWorkflowStatus.sent_final_notice)

    # Test that the process still picks up subscriptions with drastically out of date statuses and fast-forwards them.
    def test_subscriptions_due_today_with_older_status(self):
        # Create subscription with end_date 0 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(0))

        # Create a workflow state that is drastically out of date by multiple statuses
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_four_week_notice)

        process = NotifySubscriptionsDueToday()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_final_notice)

    # TODO: def test_free_subscriptions(self):

    # TODO: def test_expired_and_converted_subscriptions(self):

    # Happy path for subscriptions due in seven days.
    def test_subscriptions_due_in_seven_days_process(self):
        # Create subscription with end_date 7 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(7))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_two_week_notice)

        process = NotifySubscriptionsDueInSevenDays()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_one_week_notice)

    # TODO: def test_subscriptions_due_in_seven_days_process_with_no_subscriptions_due(self):

    def test_subscriptions_due_in_fourteen_days_process(self):
        # Create subscription with end_date 14 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(14))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.sent_four_week_notice)

        process = NotifySubscriptionsDueInFourteenDays()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_two_week_notice)

    # TODO: def test_subscriptions_due_in_fourteen_days_process_with_no_subscriptions_due(self):

    def test_subscriptions_due_in_twenty_eight_days_process(self):
        # Create subscription with end_date 28 days from now.
        subscription = self.create_subscription(self.account, end_date=days_later(28))
        workflow_state = self.create_conversion_workflow_state(subscription,
                                                               ConversionWorkflowStatus.ok)

        process = NotifySubscriptionsDueInTwentyEightDays()
        process.process()

        workflow_state.refresh()
        self.assertEqual(workflow_state.status, ConversionWorkflowStatus.sent_four_week_notice)

    # TODO: def test_subscriptions_due_in_twenty_eight_days_process_with_no_subscriptions_due(self):
