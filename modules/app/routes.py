from flask import Blueprint
from flask_login import login_required

app_blueprint = Blueprint('app_blueprint', __name__, url_prefix="/", template_folder="templates")


@app_blueprint.route("app")
@login_required
def show_app():
    return "Hello!"
