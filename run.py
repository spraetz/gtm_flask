from flask import Flask

from modules.app.routes import app_blueprint
from modules.public.routes import public_blueprint
from modules.models.user import User
from modules.models.database import db
import os
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(os.environ['environment'])

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


app.register_blueprint(public_blueprint)
app.register_blueprint(app_blueprint)
db.init_app(app)


if __name__ == '__main__':
    app.run()
