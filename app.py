from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello {}!'.format(app.config["ENVIRONMENT"])


if __name__ == '__main__':
    app.config["ENVIRONMENT"] = os.environ['environment']
    app.run()
