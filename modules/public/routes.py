from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user

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
    form = LoginForm()
    if form.validate_on_submit():
        user_to_log_in = User.query.filter_by(email="admin@gtmarketing.com").filter_by(password="123456").first()
        print user_to_log_in
        login_user(user_to_log_in)
        return redirect(url_for("app_blueprint.show_app"))
    return render_template("login.html", form=form)


@public_blueprint.route("bootstrap")
def bootstrap_database():
    print "IM in here"
    admin_user = User.query.filter_by(email="admin@gtmarketing.com").first()

    # If we don't find an admin user, create one.
    if not admin_user:
        User.create_user(email="admin@gtmarketing.com", password="123456")
        return "User not found, therefore I created one!"

    return "User found.  No op."
