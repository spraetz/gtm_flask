import gtm_email
from modules.models.account import Account
from modules.models.workflow import ConversionWorkflow, ConversionWorkflowStatus
from modules.workflow.base_process import BaseProcess


class NotifySubscriptionsDueToday(BaseProcess):

    next_status = ConversionWorkflowStatus.sent_final_notice

    @staticmethod
    def get_items_to_process():
        return ConversionWorkflow.get_subscriptions_to_send_final_notice()

    def do_work(self, subscription):
        gtm_email.send_conversion_email(Account.get_by_id(subscription.account_id), subscription)


class NotifySubscriptionsDueInSevenDays(BaseProcess):

    next_status = ConversionWorkflowStatus.sent_one_week_notice

    @staticmethod
    def get_items_to_process():
        return ConversionWorkflow.get_subscriptions_to_send_one_week_notice()

    def do_work(self, subscription):
        gtm_email.send_conversion_email(Account.get_by_id(subscription.account_id), subscription)


class NotifySubscriptionsDueInFourteenDays(BaseProcess):

    next_status = ConversionWorkflowStatus.sent_two_week_notice

    @staticmethod
    def get_items_to_process():
        return ConversionWorkflow.get_subscriptions_to_send_two_week_notice()

    def do_work(self, subscription):
        gtm_email.send_conversion_email(Account.get_by_id(subscription.account_id), subscription)


class NotifySubscriptionsDueInTwentyEightDays(BaseProcess):

    next_status = ConversionWorkflowStatus.sent_four_week_notice

    @staticmethod
    def get_items_to_process():
        return ConversionWorkflow.get_subscriptions_to_send_four_week_notice()

    def do_work(self, subscription):
        gtm_email.send_conversion_email(Account.get_by_id(subscription.account_id), subscription)
