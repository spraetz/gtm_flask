from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput

from modules.models.account import Account
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
