from modules.workflow.subscription_conversion import NotifySubscriptionsDueToday


class DailyCron:

    def __init__(self):
        self.notify_subscriptions_due_today = NotifySubscriptionsDueToday()

    def run(self):
        self.notify_subscriptions_due_today.process()
