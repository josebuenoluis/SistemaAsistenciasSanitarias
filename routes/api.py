from flask import jsonify,Blueprint,request
from flask_login import login_required
from services import mariadb_service as db_service
api = Blueprint("api",__name__)

@api.route("/api/plantas", methods=["GET"])
@login_required
def obtener_plantas():
    plantas = db_service.obtener_plantas()
    return jsonify([planta.to_dict() for planta in plantas])

@api.route("/api/asistentes", methods=["GET"])
@login_required
def obtener_asistentes():
    asistentes = db_service.obtener_asistentes()
    return jsonify([asistente.to_dict() for asistente in asistentes])

@api.route("/api/asistentes/estadisticas", methods=["GET"])
@api.route("/api/asistentes/estadisticas/<int:n_planta>", methods=["GET"])
@login_required
def obtener_asistentes_estadisticas(n_planta:int=0):
    desde = request.args.get("desde","")
    hasta = request.args.get("hasta","")
    if desde != "" and hasta != "" and n_planta != 0:
        asistentes_asistencias = db_service.asistencias_atendidas_asistente_planta(n_planta,desde,hasta)
    elif n_planta != 0 and desde == "" and hasta == "":
        asistentes_asistencias = db_service.asistencias_atendidas_asistente_planta(n_planta)
    elif desde != "" and hasta != "" and n_planta == 0:
        asistentes_asistencias = db_service.asistencias_atendidas_asistente(desde,hasta)
    else:
        asistentes_asistencias = db_service.asistencias_atendidas_asistente()
    return asistentes_asistencias

@api.route("/api/asistencias",methods=["GET"])
@api.route("/api/asistencias/<int:n_planta>",methods=["GET"])
@login_required
def obtener_asistencias(n_planta:int=0):
    if n_planta != 0:
        asistencias = db_service.obtener_asistencias_planta(n_planta)
    else:
        asistencias = db_service.obtener_asistencias()
        
    return jsonify([ {
            "id":asistencia[0],
            "habitacion_fk":asistencia[1],
            "cama_fk":asistencia[2],
            "fecha_llamada":asistencia[4],
            "fecha_presencia":asistencia[5],
            "asistente_fk":asistencia[6],
            "estado":asistencia[3]
        } for asistencia in asistencias])

@api.route("/api/asistencias/plantas",methods=["GET"])
@login_required
def obtener_asistencias_plantas():
    desde = request.args.get("desde","")
    hasta = request.args.get("hasta","")
    if desde != "" and hasta != "":
        asistencias = db_service.obtener_conteo_asistencias_planta(desde,hasta)
    else:
        asistencias = db_service.obtener_conteo_asistencias_planta()
    return asistencias

@api.route("/api/asistencias/conteo",methods=["GET"])
@api.route("/api/asistencias/conteo/<int:n_planta>",methods=["GET"])
@login_required
def asistencias_conteo(n_planta:int=0):
    desde = request.args.get("desde","")
    hasta = request.args.get("hasta","")
    if n_planta != 0 and desde != "" and hasta != "":
        conteo_asistencias = db_service.conteo_asistencias_planta(n_planta,desde,hasta)
    elif n_planta != 0 and desde == "" and hasta == "":
        conteo_asistencias = db_service.conteo_asistencias_planta(n_planta)
    elif desde != "" and hasta != "" and n_planta == 0:
        conteo_asistencias = db_service.conteo_asistencias(desde,hasta)
    else:
        conteo_asistencias = db_service.conteo_asistencias()
    return conteo_asistencias

@api.route("/api/asistencias/historico",methods=["GET"])
@login_required
def asistencias_historico():
    desde = request.args.get("desde","")
    hasta = request.args.get("hasta","")
    if desde != "" and hasta != "":
        asistencias_historico = db_service.obtener_historico(desde,hasta)
    else:
        asistencias_historico = db_service.obtener_historico()
    return asistencias_historico

@api.route("/api/habitaciones/asistencias/conteo")
@login_required
def obtener_conteo_llamadas_habitaciones():
    desde = request.args.get("desde","")
    hasta = request.args.get("hasta","")
    habitaciones_asistencias = db_service.obtener_llamados_habitaciones(desde,hasta)
    resultado_dict = [
        {
            "habitacion":habitacion[0],
            "conteo_llamadas":habitacion[1]
        } for habitacion in habitaciones_asistencias
    ]
    return resultado_dict

@api.route("/api/asistencias/porcentaje")
@login_required
def calcular_porcentaje_asistencias():
    desde = request.args.get("desde","")
    hasta = request.args.get("hasta","")
    porcentajes_asistencias = db_service.calcular_porcentaje_asistencias_totales(desde,hasta)
    return porcentajes_asistencias

@api.route("/api/asistencias/exportar/filtros",methods=["POST"])
@login_required
def obtener_asistencias_filtros():
    filtros = request.get_json()
    if filtros != "" or filtros != None:
        asistencias = db_service.obtener_asistencias_filtros(filtros)
        if asistencias != None:
            return jsonify([asistencia.to_dict() for asistencia in asistencias])
        else:
            return jsonify([])  
    else:
        return jsonify([])
    
@api.route("/api/asistencias/dispositivos/camas")
@login_required
def obtener_camas_habitacion():
    numeroHabitacion = request.args.get("numerohabitacion","")
    if numeroHabitacion != "":
        camas = db_service.obtener_camas_habitacion(numeroHabitacion)
        return jsonify([cama.to_dict() for cama in camas])
    else:
        camas = db_service.obtener_camas()
        return jsonify([cama.to_dict() for cama in camas])

@api.route("/api/habitaciones")
@login_required
def obtener_habitaciones():
    habitaciones = db_service.obtener_habitaciones()
    return jsonify([habitacion.to_dict() for habitacion in habitaciones])

@api.route("/api/dispositivos")
@login_required
def obtener_dispositivos():
    dispositivos = db_service.obtener_dispositivos()
    return dispositivos
