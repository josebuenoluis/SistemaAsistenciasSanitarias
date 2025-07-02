from flask import render_template,Blueprint,request,send_file,jsonify,session,redirect,url_for
from services import mariadb_service as db_service
from flask_login import login_required
from utils.utilidades_csv import exportarCSV
from os import path
from utils.security import Security
from io import BytesIO

asistencias = Blueprint("asistencias",__name__)

@asistencias.route("/asistencias",methods=["GET"])
def historico_asistencias_pendientes():
    # Cargar cookie y sino mandar a login Asistentes
    cookie = session.get("token")
    #llamamos a metodo de security y le pasamos la cookie_token
    if Security.verify_token_cookie(cookie):
        cookie_decode = Security.decode_token_cookie(cookie)
        asistente = db_service.getAsistente(cookie_decode["username"],cookie_decode["codigo"])
        if asistente != None:
            asistencias_planta = db_service.obtener_asistencias_planta_24(asistente.planta_fk)
            return render_template("asistencias.html",asistencias=asistencias_planta,asistente=asistente)
        else:
            return render_template("asistencias-enroll.html")   
    else:
        return render_template("asistencias-enroll.html")
        

@asistencias.route("/asistencias/historico", methods=["GET"])
@login_required
def historico_asistencias():
    return render_template("asistencias-historico.html")

@asistencias.route("/asistencias/consultas", methods=["GET"])
@login_required
def consultas_asistencias():
    return render_template("asistencias-consultas.html")

@asistencias.route("/asistencias/exportar", methods=["GET","POST"])
@login_required
def exportar_asistencias():
    if request.method == "GET":
        asistencias = db_service.obtener_asistencias()
        plantas = db_service.obtener_plantas()
        return render_template("exportar-datos.html",asistencias=asistencias,plantas=plantas)
    else:
        data = request.get_json()
        success = False
        if data:
            buffer = BytesIO()
            buffer_escrito = exportarCSV(data,buffer)
            success = True
            return send_file(
                buffer_escrito,
                as_attachment=True,
                download_name="archivo.csv"
            )

        return {"success":success}

@asistencias.route("/asistencias/dispositivos", methods=["GET","POST","PUT","DELETE"])
@login_required
def dispositivos():
    if request.method == "GET":
        habitaciones = db_service.obtener_habitaciones()
        dispositivos = db_service.obtener_dispositivos()
        return render_template("asistencias-dispositivos.html",habitaciones=habitaciones,dispositivos=dispositivos)
    elif request.method == "PUT":
        data = request.get_json()
        if db_service.actualizar_dispositvos(data):
            return jsonify({'success': True, 'message': ["Dispositivos actualizados correctamente"]})    
        else:
            return jsonify({'success': False, 'message': ["Error al actualizar dispositivos"]})    
    elif request.method == "DELETE":
        data = request.get_json()
        valido = db_service.eliminar_dispositivos(data)
        if valido:
            return jsonify({'success': True, 'message': ["Dispositivos eliminados correctamente"]})
        else:
            return jsonify({'success': False, 'message': ["Error al eliminar dispositivos"]})
    else:
        data = request.get_json()
        if db_service.registrar_dispositivo(tipo=data["tipo"],ip=data["ip"],puerto=data["puerto"],habitacion=data["habitacion"],cama_id=data["cama"]):
            return jsonify({'success': True, 'message': ["Dispositivo registrado correctamente"]})
        else:
            return jsonify({'success': False, 'message': ["Error al registrar dispositivo"]})