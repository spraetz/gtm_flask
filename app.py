from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(os.environ['environment'])
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from models import *


@app.route('/')
def hello_world():

    #foo = models.Test()
    #foo.str = "asdfasfds"
    #db.session.add(foo)
    #db.session.commit()
    foo = Test.query.all()
    return 'Hello {}!'.format(len(foo))


if __name__ == '__main__':
    app.run()
