import StringIO
import csv

from flask import Blueprint, render_template, request, url_for, redirect, make_response
from flask_login import login_required

from forms import AccountForm
from modules.models.account import Account

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
    form = AccountForm(request.form)

    return render_template("account.html", form=form, account=account)


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


@app_blueprint.route("export", methods=["POST"])
def do_export_accounts():
    si = StringIO.StringIO()
    cw = csv.writer(si)
    accounts = Account.query.all()

    cw.writerow(Account.get_fields())

    for account in accounts:
        cw.writerow(account.get_field_values())

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
