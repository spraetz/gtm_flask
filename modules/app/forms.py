from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput

from modules.models.account import Account
from modules.models.subscription import SubscriptionTypes
from modules.models.validators import Unique


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


class SubscriptionForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    account_id = IntegerField(widget=HiddenInput())
    type = SelectField("Type", choices=[(SubscriptionTypes.trial, "Trial"),
                                        (SubscriptionTypes.paid, "Paid"),
                                        (SubscriptionTypes.free, "Free")])
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    text_alerts = BooleanField("Text Alerts")
    voice_alerts = BooleanField("Voice Alerts")
    voice_alerts_phone = SelectField("Voice Alerts Phone", choices=[("home_phone", "Home Phone"),
                                                                    ("mobile_phone", "Mobile Phone")])
