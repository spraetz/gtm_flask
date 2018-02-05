from flask import Flask
from database import db
import os
from flask_login import LoginManager, login_required
from routes.public import public_blueprint

app = Flask(__name__)
app.config.from_object(os.environ['environment'])

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    import models.user
    return models.user.User.query.filter_by(id=user_id).first()
    pass


app.register_blueprint(public_blueprint)
db.init_app(app)

@app.route("/app")
@login_required
def show_app():
    return "Hello!"


if __name__ == '__main__':
    app.run()
