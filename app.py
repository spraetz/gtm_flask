from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, login_user, login_required
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(os.environ['environment'])
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return models.user.User.query.filter_by(id=user_id).first()


import models.user


@app.route('/', methods=["GET", "POST"])
def show_index():
    form = LoginForm()

    return render_template("index.html", form=form)


@app.route("/login")
def show_login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/login", methods=["POST"])
def do_login():
    form = LoginForm()
    if form.validate_on_submit():
        user_to_log_in = models.user.User.query.filter_by(email="admin@gtmarketing.com").filter_by(password="123456").first()
        login_user(user_to_log_in)
        return redirect(url_for("show_app"))
    return render_template("login.html", form=form)


@app.route("/app")
@login_required
def show_app():
    return "Hello!"


@app.route("/bootstrap")
def bootstrap_database():
    print "IM in here"
    admin_user = models.user.User.query.filter_by(email="admin@gtmarketing.com").first()

    # If we don't find an admin user, create one.
    if not admin_user:
        models.user.User.create_user(email="admin@gtmarketing.com", password="123456")
        return "User not found, therefore I created one!"

    return "User found.  No op."


if __name__ == '__main__':
    app.run()
