from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from modules.models.account import Account


class AccountForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    home_phone = StringField("Phone", validators=[Length(Account.home_phone.property.columns[0].type.length,
                                                         Account.home_phone.property.columns[0].type.length,
                                                         "Phone numbers must be 10 numbers (eg: 8152734354)")])
    mobile_phone = StringField("Mobile", validators=[Length(Account.home_phone.property.columns[0].type.length,
                                                            Account.home_phone.property.columns[0].type.length,
                                                            "Phone numbers must be 10 numbers (eg: 8152734354)")])

