from flask import render_template,Blueprint,request,jsonify,redirect,url_for,flash
from services import mariadb_service as db_service
from flask_login import login_user,logout_user
from models.db import db

login = Blueprint("login",__name__)


@login.route("/login", methods=["GET","POST"])
def iniciar_sesion():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        logged = db_service.login(username,password)
        if logged != None:
            login_user(logged)
            return redirect(url_for("asistentes.modificar_asistente"))
        else:
            flash("Usuario o contraseña son incorrectos")
            return render_template("login.html")
    else:
        return render_template("login.html")

@login.route("/logout",methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("login.iniciar_sesion"))