import requests
from requests.auth import HTTPBasicAuth
import flask
import json


def add_to_list(account):
    url = "https://us18.api.mailchimp.com/3.0/lists/{}".format(flask.current_app.config["MAILCHIMP_LIST_ID"])
    header = {"content-type": "application/json"}
    data = {
        "members": [
            {
                "email_address": account.email,
                "status": "subscribed"
            }
        ],
        "update_existing": True
    }

    # Mailchimp is really stupid and doesn't care what username you use, so "foo" it is.
    auth = HTTPBasicAuth("foo", flask.current_app.config["MAILCHIMP_API_KEY"])

    # TODO: Set up mocking properly using http://requests-mock.readthedocs.io/en/latest/mocker.html#class-decorator
    if not flask.current_app.config["TESTING"]:
        resp = requests.post(url, data=json.dumps(data), headers=header, auth=auth)
        resp.raise_for_status()


def remove_from_list(account):
    url = "https://us18.api.mailchimp.com/3.0/lists/{}".format(flask.current_app.config["MAILCHIMP_LIST_ID"])
    header = {"content-type": "application/json"}
    data = {
        "members": [
            {
                "email_address": account.email,
                "status": "unsubscribed"
            }
        ],
        "update_existing": True
    }

    # Mailchimp is really stupid and doesn't care what username you use, so "foo" it is.
    auth = HTTPBasicAuth("foo", flask.current_app.config["MAILCHIMP_API_KEY"])

    if not flask.current_app.config["TESTING"]:
        resp = requests.post(url, data=json.dumps(data), headers=header, auth=auth)
        resp.raise_for_status()
