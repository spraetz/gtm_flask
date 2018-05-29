import gtm_email
from modules.models.account import Account
from modules.models.workflow import ConversionWorkflow, ConversionWorkflowStatus


class NotifySubscriptionsDueToday:
    def __init__(self):
        self.workflow_states = self.get_items_to_process()

    next_status = ConversionWorkflowStatus.sent_final_notice

    @staticmethod
    def get_items_to_process():
        return ConversionWorkflow.get_items_due_today()

    def process(self):
        for workflow_state in self.workflow_states:
            subscription = workflow_state.get_subscription()

            gtm_email.send_conversion_email(Account.get_by_id(subscription.account_id), subscription)

            workflow_state.status = self.next_status
            workflow_state.save()