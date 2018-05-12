import datetime

from lib import gtm_email
from modules.models.account import Account
from modules.models.subscription import Subscription, SubscriptionTypes


class DailyCron:

    def __init__(self):
        # We want to email all subscriptions @ 28 days, 21 days, 14 days, and 7 days before end_date
        self.subscriptions = self.get_subscriptions_to_contact()

    def run(self):

        for subscription in self.subscriptions:
            if subscription.type == SubscriptionTypes.trial:
                # For trial subscriptions, send a conversion attempt email
                gtm_email.send_conversion_email(Account.get_by_id(subscription.account_id), subscription)

            elif subscription.type == SubscriptionTypes.paid:
                # For paid subscriptions, send a renewal attempt email
                gtm_email.send_renewal_email(Account.get_by_id(subscription.account_id), subscription)

            elif subscription.type == SubscriptionTypes.free:
                # For free subscriptions, do nothing.
                pass
            else:
                raise Exception("Found a subscription of unknown type.")

    def get_subscriptions_to_contact(self):
        subscriptions = Subscription.query.filter((Subscription.end_date == self.days_later(28)) |
                                                  (Subscription.end_date == self.days_later(14)) |
                                                  (Subscription.end_date == self.days_later(7)) |
                                                  (Subscription.end_date == self.days_later(0))).all()

        return subscriptions

    @staticmethod
    def days_later(days):
        return datetime.date.today() + datetime.timedelta(days=days)
