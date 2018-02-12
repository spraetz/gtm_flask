import os

from flask import Flask
from flask_login import LoginManager

from modules.app.routes import app_blueprint
from modules.models.database import db
from modules.models.user import User
from modules.public.routes import public_blueprint
from modules.errors.handlers import register_error_handlers


def create_app():
    application = Flask(__name__)

    # This sets the config to whatever was passed in
    application.config.from_object(os.environ['environment'])

    # Register blueprints
    application.register_blueprint(public_blueprint)
    application.register_blueprint(app_blueprint)
    register_error_handlers(application)

    # Instantiate Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    return application


app = create_app()
db.init_app(app)

if __name__ == '__main__':
    app.run()
