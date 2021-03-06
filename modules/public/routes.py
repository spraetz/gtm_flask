from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user

from forms import LoginForm
from modules.models.user import User

public_blueprint = Blueprint('public_blueprint', __name__, url_prefix="/", template_folder="templates")


@public_blueprint.route("")
def show_index():
    return render_template("index.html")


@public_blueprint.route("login")
def show_login():
    form = LoginForm()
    return render_template("login.html", form=form)


@public_blueprint.route("login", methods=["POST"])
def do_login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user_to_log_in = User.query.filter_by(email=form.email.data).filter_by(password=form.password.data).first()
        if user_to_log_in:
            login_user(user_to_log_in)
            return redirect(url_for("app_blueprint.show_home"))
    return render_template("login.html", form=form), 400


# TODO: Needs to be tested.
@public_blueprint.route("logout")
def do_logout():
    logout_user()
    return redirect(url_for("public_blueprint.show_login"))


@public_blueprint.route("bootstrap")
def do_bootstrap_database():
    admin_user = User.query.filter_by(email="admin@gtmarketing.com").first()

    # If we don't find an admin user, create one.
    if not admin_user:
        User.create_user(email="admin@gtmarketing.com", password="123456")
        return "User not found, therefore I created one!"

    return abort(404)
