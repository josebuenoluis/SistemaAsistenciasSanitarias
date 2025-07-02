from flask import render_template,Blueprint,request,jsonify
from services import mariadb_service as db_service
from flask_login import login_required
from models.db import db
asistentes = Blueprint("asistentes",__name__)

@asistentes.route("/asistentes/crear", methods=["GET","POST"])
@login_required
def crear_asistente():
    if request.method == "GET":
        plantas = db_service.obtener_plantas()
        return render_template("crear-asistente.html", plantas=plantas)
    else:
        data = request.get_json()
        asistente_data = {
            "nif": data["nif"],
            "nombre": data["nombre"],
            "telefono": data["telefono"],
            "codigo": data["codigo"],
            "planta": data["planta"]
        }
        valido,mensajes_error = db_service.crear_asistente(asistente_data)
        if valido:
            return jsonify({'success': True, 'message': ["Asistente creado correctamente"]})
        else:
            return jsonify({'success': False, 'message': mensajes_error})


@asistentes.route("/asistentes/modificar", methods=["GET","PUT","DELETE"])
@login_required
def modificar_asistente():
    if request.method == "GET":
        plantas = db_service.obtener_plantas()
        asistentes = db_service.obtener_asistentes()
        return render_template("asistentes-modificar.html",plantas=plantas,asistentes=asistentes)
    elif request.method == "DELETE":
        data = request.get_json()
        valido = db_service.eliminar_asistentes(data)
        if valido:
            return jsonify({'success': True, 'message': ["Asistentes eliminados correctamente"]})
        else:
            return jsonify({'success': False, 'message': ["Error al eliminar asistentes"]})
    else:
        data = request.get_json()
        valido = db_service.modificar_asistentes(data)
        if valido:
            return jsonify({'success': True, 'message': ["Asistentes modificados correctamente"]})
        else:
            return jsonify({'success': False, 'message': ["Error al modificar asistentes"]})

@asistentes.route("/asistentes/estadisticas", methods=["GET"])
@login_required
def estadisticas_asistente():
    asistentes_asistencias = db_service.asistencias_atendidas_asistente()
    plantas = db_service.obtener_plantas()
    return render_template("asistentes-estadisticas.html",
    asistentes_asistencias=asistentes_asistencias,plantas=plantas)

