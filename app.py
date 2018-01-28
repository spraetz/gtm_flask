from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['environment'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gtm_development'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# from models import Test

@app.route('/')
def hello_world():

    #foo = models.Test()
    #foo.str = "asdfasfds"
    #db.session.add(foo)
    #db.session.commit()
    # foo = Test.query.all()
    return 'Hello {}!'.format(app.config["NAME"])


if __name__ == '__main__':
    app.run()
