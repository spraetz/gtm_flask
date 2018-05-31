from modules.workflow.subscription_conversion import NotifySubscriptionsDueToday, NotifySubscriptionsDueInSevenDays, \
    NotifySubscriptionsDueInFourteenDays, NotifySubscriptionsDueInTwentyEightDays


class DailyCron:

    def __init__(self):
        self.notify_subscriptions_due_today = NotifySubscriptionsDueToday()
        self.notify_subscriptions_due_in_seven_days = NotifySubscriptionsDueInSevenDays()
        self.notify_subscriptions_due_in_fourteen_days = NotifySubscriptionsDueInFourteenDays()
        self.notify_subscriptions_due_in_twenty_eight_days = NotifySubscriptionsDueInTwentyEightDays()

    def run(self):
        self.notify_subscriptions_due_today.process()
        self.notify_subscriptions_due_in_seven_days.process()
        self.notify_subscriptions_due_in_fourteen_days.process()
        self.notify_subscriptions_due_in_twenty_eight_days.process()
