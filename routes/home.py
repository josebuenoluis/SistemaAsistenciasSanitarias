from flask import render_template,Blueprint
from services import mariadb_service as db_service
home = Blueprint("home",__name__)

@home.route("/")
def index():
    return render_template("panelhab.html")