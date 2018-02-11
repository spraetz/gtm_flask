import os

from flask import Flask
from flask_login import LoginManager

from modules.app.routes import app_blueprint
from modules.models.database import db
from modules.models.user import User
from modules.public.routes import public_blueprint


def create_app():
    application = Flask(__name__)
    application.config.from_object(os.environ['environment'])
    application.register_blueprint(public_blueprint)
    application.register_blueprint(app_blueprint)

    return application


app = create_app()

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


if __name__ == '__main__':
    app.run()
