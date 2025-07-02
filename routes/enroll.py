from flask import render_template,Blueprint,request,jsonify,redirect,url_for,flash,session
from services import mariadb_service as db_service
from utils.security import Security
from models.db import db

enroll = Blueprint("enroll",__name__)

@enroll.route("/enroll", methods=["GET","POST"])
def login_enroll():
    if request.method == "POST":
        token = ""
        usuario = request.form["username"]
        codigo = request.form["codigo"]
        user = db_service.getAsistente(usuario,codigo)
        if user != None:
            token = Security.generate_token(user)
            session["token"] = token
            db_service.actualizar_estado_asistente(user,True)
            return redirect(url_for("asistencias.historico_asistencias_pendientes"))                 
        flash("Usuario o código son incorrectos")
        return render_template("asistencias-enroll.html")
    else:
        return render_template("asistencias-enroll.html")

@enroll.route("/desenroll",methods=["GET"])
def logout_enroll():
    cookie = session.get("token")
    cookie_decode = Security.decode_token_cookie(cookie)
    asistente = db_service.getAsistente(cookie_decode["username"],cookie_decode["codigo"])
    db_service.actualizar_estado_asistente(asistente,False)
    session.pop("token")
    return redirect(url_for("enroll.login_enroll"))