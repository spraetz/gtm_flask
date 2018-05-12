import sendgrid
from python_http_client import BadRequestsError
from sendgrid.helpers.mail import *
import flask


def send_conversion_email(account, subscription):

    personalization = Personalization()
    personalization.add_to(Email(account.email))

    personalization.add_substitution(Substitution("%first_name%", account.first_name))
    personalization.add_substitution(Substitution("%end_date%", subscription.end_date.strftime("%B %e, %Y")))
    personalization.add_substitution(Substitution("%subscription_cost%", "${}.00".format(
        account.default_subscription_price/100)))

    personalization.add_custom_arg(CustomArg("subscription_id", str(subscription.id)))
    personalization.add_custom_arg(CustomArg("account_id", str(account.id)))

    send_email_from_template(template_id="3acb9944-22c3-4f11-b7a0-6c7458f2c2a9", personalization=personalization)


def send_renewal_email(account, subscription):

    personalization = Personalization()
    personalization.add_to(Email(account.email))

    personalization.add_substitution(Substitution("%first_name%", account.first_name))
    personalization.add_substitution(Substitution("%end_date%", subscription.end_date.strftime("%B %e, %Y")))
    personalization.add_substitution(Substitution("%subscription_cost%", "${}.00".format(
        account.default_subscription_price/100)))

    send_email_from_template(template_id="d0f16c3f-b7fd-4ef3-b833-ee000e9670fe", personalization=personalization)


def send_email_from_template(template_id, personalization, from_email="bill@graintracker.com"):

    # Configure the client
    sg = sendgrid.SendGridAPIClient(apikey=flask.current_app.config["SENDGRID_API_KEY"])

    email = Mail()
    email.from_email = Email(from_email)
    email.template_id = template_id

    personalization.add_bcc(Email("spraetz+gtm@gmail.com"))
    # TODO: Add bill@graintracker.com to bcc.

    email.add_personalization(personalization)

    if not flask.current_app.config["TESTING"]:
        try:
            sg.client.mail.send.post(request_body=email.get())
        except BadRequestsError as e:
            print e.message
            raise e

    return email.get()
