import StringIO
import csv

import datetime
from flask import Blueprint, render_template, request, url_for, redirect, make_response
from flask_login import login_required

from forms import AccountForm, SubscriptionForm
from modules.models.account import Account
from modules.models.subscription import Subscription, SubscriptionStatuses

app_blueprint = Blueprint('app_blueprint', __name__, url_prefix="/app/", template_folder="templates")


@app_blueprint.route("")
@login_required
def show_home():
    return render_template("home.html", context={})


@app_blueprint.route("accounts")
@login_required
def show_accounts():
    accounts = Account.query.all()

    return render_template("list_accounts.html", accounts=accounts)


@app_blueprint.route("accounts/<account_id>")
@login_required
def show_account(account_id):
    account = Account.get_by_id(account_id)
    subscriptions = account.get_subscriptions()
    form = AccountForm(obj=account)

    return render_template("account.html", form=form, account=account, subscriptions=subscriptions)


@app_blueprint.route("accounts/<account_id>", methods=["POST"])
@login_required
def do_save_account(account_id):
    account = Account.get_by_id(account_id)

    form = AccountForm(request.form)
    form.populate_obj(account)

    if form.validate_on_submit():
        account.save()
        return redirect(url_for("app_blueprint.show_accounts"))

    return render_template("account.html", form=form, account=account), 400


@app_blueprint.route("accounts/create")
@login_required
def show_create_account():
    form = AccountForm(request.form)
    return render_template("account.html", form=form)


@app_blueprint.route("accounts/create", methods=["POST"])
@login_required
def do_create_account():
    form = AccountForm(request.form)
    account = Account()
    form.populate_obj(account)

    if form.validate_on_submit():
        account.save()
        return redirect(url_for("app_blueprint.show_accounts"))

    return render_template("account.html", form=form), 400


@app_blueprint.route("accounts/<account_id>/delete", methods=["POST"])
@login_required
def do_delete_account(account_id):
    account = Account.get_by_id(account_id)
    account.delete()
    return redirect(url_for("app_blueprint.show_accounts"))


@app_blueprint.route("accounts/export", methods=["POST"])
def do_export_accounts():
    si = StringIO.StringIO()
    cw = csv.writer(si)
    accounts = Account.query.all()

    cw.writerow(Account.get_fields())

    for account in accounts:
        cw.writerow(account.get_field_values())

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename={}-accounts.csv".format(datetime.datetime.today().
                                                                                          isoformat())
    output.headers["Content-type"] = "text/csv"
    return output


@app_blueprint.route("accounts/<account_id>/subscriptions/create")
@login_required
def show_create_subscription(account_id):
    account = Account.get_by_id(account_id)
    form = SubscriptionForm(request.form)

    return render_template("subscription.html", account=account, form=form)


@app_blueprint.route("accounts/<account_id>/subscriptions/create", methods=["POST"])
@login_required
def do_create_subscription(account_id):
    form = SubscriptionForm(request.form)
    account = Account.get_by_id(account_id)
    subscription = Subscription(status=SubscriptionStatuses.active)
    form.populate_obj(subscription)

    if form.validate_on_submit():
        subscription.save()
        return redirect(url_for("app_blueprint.show_account", account_id=account.id))

    return render_template("subscription.html", account=account, form=form), 400


@app_blueprint.route("accounts/<account_id>/subscriptions/<subscription_id>")
@login_required
def show_subscription(account_id, subscription_id):
    account = Account.get_by_id(account_id)
    subscription = Subscription.get_by_id(subscription_id)
    form = SubscriptionForm(obj=subscription)
    return render_template("subscription.html", form=form, account=account, subscription=subscription)


@app_blueprint.route("accounts/<account_id>/subscriptions/<subscription_id>", methods=["POST"])
@login_required
def do_save_subscription(account_id, subscription_id):
    account = Account.get_by_id(account_id)
    subscription = Subscription.get_by_id(subscription_id)
    form = SubscriptionForm(request.form)
    form.populate_obj(subscription)

    if form.validate_on_submit():
        subscription.save()
        return redirect(url_for("app_blueprint.show_account", account_id=account.id))

    return render_template("subscription.html", form=form, account=account, subscription=subscription)


# TODO: Remove
@app_blueprint.route("subscriptions")
@login_required
def show_subscriptions():
    subscriptions = Subscription.query.all()
    return render_template("list_subscriptions.html", subscriptions=subscriptions)
