from flask import render_template,Blueprint,request,jsonify,redirect,url_for,flash,session
from utils.security import Security
from services import mariadb_service as db_service
from services import pushover_service
from models.db import db
import requests

pushover = Blueprint("pushover",__name__)

@pushover.route("/llamada/<int:habitacion>/<string:cama>")
def enviar_mensaje(habitacion:int=0,cama:str=""):
    habitacion = request.url.split("/")[4]
    cama = request.url.split("/")[5]
    asistencia = db_service.crear_asistencia(habitacion,cama)
    if asistencia != False:
        pushover_service.enviar_mensaje({"title":"ASISTENCIA","message":f'''<html>Solicitud de asistencia en habitación <b><font color="red">{habitacion}</font></b> y cama <b><font color="red">{cama}</font></b>
                                         <a href="http://192.168.0.45:8000/atender/{asistencia.id}">Atender solicitud de asistencia</a></html>''',"html":1,"priority":2,
                                         "retry":30,"expire":180,"sound":"persistent"})
    
        return jsonify({"success":True})
    else:
        return jsonify({"success":False})
    
@pushover.route("/atender/<int:id>")
def atender_asistencia(id:int):
    cookie = session.get("token")
    if Security.verify_token_cookie(cookie):
        cookie_decode = Security.decode_token_cookie(cookie)
        asistente = db_service.getAsistente(cookie_decode["username"],cookie_decode["codigo"])
        # Obtenemos el rele asociado a la cama para activar con 
        if asistente != None:
            if db_service.atender_asistencia(id,asistente) == True:
                asistencia = db_service.obtener_asistencia(id)
                rele_cama = db_service.consultar_rele_cama(asistencia.habitacion_fk,asistencia.cama_fk)
                try:
                    response = requests.get(f"http://{rele_cama.ip}:{rele_cama.puerto}/relay/0?turn=on",timeout=5)
                except Exception as e:
                    print("Error al enviar señal a relé: ",e)
                return render_template("asistencia-atendida.html",asistencia=asistencia,asistente=asistente)
            else:
                return render_template("asistencia-no-atendida.html",asistente=asistente)
        else:
            return redirect(url_for("asistencias.historico_asistencias_pendientes"))  
    else:
        return redirect(url_for("enroll.login_enroll"))

@pushover.route("/presencia/<int:habitacion>/<string:cama>")
def presencia_asistencia(habitacion:int=0,cama:str=""):
    presencia = db_service.presencia_asistencia(habitacion,cama)
    rele_cama = db_service.consultar_rele_cama(habitacion,cama)
    try:
        response = requests.get(f"http://{rele_cama.ip}:{rele_cama.puerto}/relay/0?turn=off",timeout=5)
    except Exception as e:
        print("Error al enviar señal a relé: ",e)
    if presencia == True:
        return jsonify({"success":True})
    else:
        return jsonify({"success":False})