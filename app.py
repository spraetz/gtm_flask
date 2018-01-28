from flask import Flask
import os

app = Flask(__name__)

settings = {}


@app.route('/')
def hello_world():
    return 'Hello {}!'.format(settings.get("environment", "omg"))


if __name__ == '__main__':
    settings["environment"] = os.environ.get("environment", "wtf")
    app.run()
