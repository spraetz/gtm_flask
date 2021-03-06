from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput

from modules.models.account import Account
from modules.models.subscription import Subscription, SubscriptionTypes, SubscriptionStatuses
from modules.models.validators import Unique, GreaterThan, DaysBetween


class AccountForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    email = StringField("Email", validators=[DataRequired(), Unique(Account, "Duplicate email detected.")])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    home_phone = StringField("Phone", validators=[Length(Account.home_phone.property.columns[0].type.length,
                                                         Account.home_phone.property.columns[0].type.length,
                                                         "Phone numbers must be 10 numbers (eg: 8152734354)")])
    mobile_phone = StringField("Mobile", validators=[Length(Account.home_phone.property.columns[0].type.length,
                                                            Account.home_phone.property.columns[0].type.length,
                                                            "Phone numbers must be 10 numbers (eg: 8152734354)")])
    street_address = StringField("Street")
    secondary_address = StringField("Secondary")
    city = StringField("City")
    state = StringField("State")
    zip_code = StringField("Zip Code")
    default_subscription_price = IntegerField("Price")


class SubscriptionForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    account_id = IntegerField(widget=HiddenInput())
    type = SelectField("Type", choices=[(SubscriptionTypes.trial, "Trial"),
                                        (SubscriptionTypes.paid, "Paid"),
                                        (SubscriptionTypes.free, "Free")])
    status = SelectField("Status", choices=[(SubscriptionStatuses.active, "Active"),
                                            (SubscriptionStatuses.expired, "Expired"),
                                            (SubscriptionStatuses.converted, "Converted")])
    start_date = DateField("Start Date")
    end_date = DateField("End Date",
                         validators=[GreaterThan("start_date", "End Date must be after Start Date"),
                                     DaysBetween("start_date",
                                                 Subscription.MINIMUM_SUBSCRIPTION_LENGTH_DAYS,
                                                 "Subscriptions must be at least {} days long.".
                                                 format(Subscription.MINIMUM_SUBSCRIPTION_LENGTH_DAYS))])
    text_alerts = BooleanField("Text Alerts")
    voice_alerts = BooleanField("Voice Alerts")
    voice_alerts_phone = SelectField("Voice Alerts Phone", choices=[("home_phone", "Home Phone"),
                                                                    ("mobile_phone", "Mobile Phone")])
