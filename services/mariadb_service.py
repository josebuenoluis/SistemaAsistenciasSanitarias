from models.plantas_model import Plantas
from models.asistentes_model import Asistentes
from models.asistencias_model import Asistencias
from models.habitaciones_model import Habitaciones
from models.camas_model import Camas
from models.user_model import User
from models.dispositivos_model import Dispositivos
from models.db import db
from sqlalchemy import func,extract
from datetime import datetime,timedelta

def obtener_plantas() -> list[Plantas]:
    """"Función para obtener todas las plantas de la base de datos"""
    plantas = Plantas.query.all()
    return plantas

def obtener_asistentes() -> list[Asistentes]:
    """Función para obtener todos los asistentes de la base de datos"""
    asistentes = Asistentes.query.all()
    return asistentes

def crear_asistente(asistente_data:dict) -> tuple[bool, list[str]]:
    """Función para crear un asistente en la base de datos"""
    try:
        valido = False
        mensajes_error = validar_campos_asistente(asistente_data)
        if len(mensajes_error) == 0:
            asistente = Asistentes(dni=asistente_data["nif"], nombre=asistente_data["nombre"], 
            telefono=int(asistente_data["telefono"]), codigo=asistente_data["codigo"],
            planta_fk=int(asistente_data["planta"]))
            db.session.add(asistente)
            db.session.commit()
            valido = True
        return valido, mensajes_error
    except Exception as e:
        print("Mensajes de error en EXCEPTION: ", e)
        db.session.rollback()
        return False,[]

def validar_campos_asistente(asistente_data:dict) -> list[str]:
    """Función para validar los campos del asistente"""
    mensajes_error = []
    if Asistentes.query.filter_by(dni=asistente_data["nif"]).first() is not None:
        mensajes_error.append("El DNI ya existe")
    if Asistentes.query.filter_by(telefono=asistente_data["telefono"]).first() is not None:
        mensajes_error.append("El teléfono ya existe")
    if Asistentes.query.filter_by(codigo=asistente_data["codigo"]).first() is not None:     
        mensajes_error.append("El código ya existe")
    if Plantas.query.filter_by(numero=asistente_data["planta"]).first() is None:
        mensajes_error.append("La planta no existe")   
    return mensajes_error

def modificar_asistentes(asistentes_data:dict) -> bool:
    """Función para modificar múltiples asistentes"""
    try:
        for asistente in asistentes_data:
            asistente_db = Asistentes.query.filter_by(dni=asistente["nif"]).first()
            if asistente_db is not None:
                asistente_db.nombre = asistente["nombre"]
                asistente_db.telefono = int(asistente["telefono"])
                asistente_db.codigo = asistente["codigo"]
                asistente_db.planta_fk = int(asistente["planta"]) 
                db.session.commit()
        return True
    except Exception as e:
        print("Mensajes de error en EXCEPTION: ", e)
        db.session.rollback()
        return False
    
def eliminar_asistentes(nifs_data:list) -> bool:
    """Función para eliminar múltiples asistentes"""
    try:
        for nif in nifs_data:
            asistente_db = Asistentes.query.filter_by(dni=nif).first()
            if asistente_db is not None:
                db.session.delete(asistente_db)
                db.session.commit()
        return True
    except Exception as e:
        print("Error al eliminar asistentes: ", e)
        db.session.rollback()
        return False


def obtener_asistentes_por_planta(planta:int) -> list[Asistentes]:
    """Función para obtener todos los asistentes de una planta"""
    asistentes = Asistentes.query.filter_by(planta_fk=planta).all()
    return asistentes

def asistencias_atendidas_asistente(desde="",hasta="") -> list[dict]:
    """Función para obtener las asistencias atendidas por asistente."""
    if desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        resultado = (
        db.session.query(
            Asistentes.dni,
            Asistentes.nombre,
            Asistentes.planta_fk,
            func.count(Asistencias.id).label("conteo_asistencias")
        ).join(Asistencias, Asistentes.dni == Asistencias.asistente_fk)
            .group_by(Asistentes.dni, Asistentes.nombre, Asistentes.planta_fk)
            .filter(
                Asistencias.fecha_llamada >= desde,
                Asistencias.fecha_llamada <= hasta,
                Asistencias.estado=="atendida"
            ).all()
        )
    else:
        resultado = (
        db.session.query(
            Asistentes.dni,
            Asistentes.nombre,
            Asistentes.planta_fk,
            func.count(Asistencias.id).label("conteo_asistencias")
        ).join(Asistencias, Asistentes.dni == Asistencias.asistente_fk)
            .group_by(Asistentes.dni, Asistentes.nombre, Asistentes.planta_fk)
            .filter(Asistencias.estado=="atendida")
            .all()
        )

    resultado_dict = [
        {
            "dni":consulta_asistencia[0],
            "nombre":consulta_asistencia[1],
            "planta":consulta_asistencia[2],
            "asistencias_atendidas":consulta_asistencia[3]

        } for consulta_asistencia in resultado
    ]
    return resultado_dict

def asistencias_atendidas_asistente_planta(n_planta,desde="",hasta="") -> list[dict]:
    """Función para obtener las asistencias atendidas por asistente por planta."""
    if n_planta != 0 and desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        resultado = (
        db.session.query(
            Asistentes.dni,
            Asistentes.nombre,
            Asistentes.planta_fk,
            func.count(Asistencias.id).label("conteo_asistencias")
        ).join(Asistencias, Asistentes.dni == Asistencias.asistente_fk)
            .group_by(Asistentes.dni, Asistentes.nombre, Asistentes.planta_fk)
            .filter(
                Asistencias.estado=="atendida",
                Asistentes.planta_fk==n_planta,
                Asistencias.fecha_llamada >= desde,
                Asistencias.fecha_llamada <= hasta
            ).all()
        )
    elif n_planta != 0 and desde == "" and hasta == "":
        resultado = (
        db.session.query(
            Asistentes.dni,
            Asistentes.nombre,
            Asistentes.planta_fk,
            func.count(Asistencias.id).label("conteo_asistencias")
        ).join(Asistencias, Asistentes.dni == Asistencias.asistente_fk)
            .group_by(Asistentes.dni, Asistentes.nombre, Asistentes.planta_fk)
            .filter(Asistencias.estado=="atendida",Asistentes.planta_fk==n_planta)
            .all()
        )

    resultado_dict = [
        {
            "dni":consulta_asistencia[0],
            "nombre":consulta_asistencia[1],
            "planta":consulta_asistencia[2],
            "asistencias_atendidas":consulta_asistencia[3]

        } for consulta_asistencia in resultado
    ]
    return resultado_dict

def obtener_asistencias_planta(planta:int) -> list[Asistencias]:
    """Función para obtener todas las asistencias de una planta."""
    asistencias = (
    db.session.query(
        Asistencias.id,
        Habitaciones.numero.label("habitacion"),
        Camas.nombre.label("cama"),
        Asistencias.estado,
        Asistencias.fecha_llamada,
        Asistencias.fecha_presencia,
        Asistencias.asistente_fk
    )
    .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero)
    .join(Camas, Asistencias.cama_fk == Camas.id)
    .filter(Habitaciones.planta_fk == planta)
    .all()
    )
    return asistencias

def obtener_asistencias_planta_24(planta:int) -> list[Asistencias]:
    """Función para obtener todas las asistencias de una planta 
    de las últimas 24 horas."""
    hace_24_horas = datetime.now() - timedelta(hours=24)
    asistencias = (
        db.session.query(
            Asistencias.id,
            Habitaciones.numero.label("habitacion"),
            Camas.nombre.label("cama"),
            Asistencias.estado,
            Asistencias.fecha_llamada
        )
        .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero)
        .join(Camas, Asistencias.cama_fk == Camas.id)
        .filter(Habitaciones.planta_fk == planta)
        .filter(Asistencias.fecha_llamada >= hace_24_horas)
        .order_by(Asistencias.id.desc())
        .all()
    )

    return asistencias

def obtener_asistencias() -> list[Asistencias]:
    """Función para obtener todas las asistencias."""
    asistencias = Asistencias.query.all()
    return asistencias

def conteo_asistencias(desde="",hasta="") -> dict:
    """Función para devolver el número de asistencias 
    atendidas y no atendidas."""
    if desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        asistencias_pendientes = Asistencias.query.filter(
            Asistencias.estado=="pendiente",
            Asistencias.fecha_llamada >= desde,
            Asistencias.fecha_llamada <= hasta,
        ).count()
        asistencias_atendidas = Asistencias.query.filter(
            Asistencias.estado=="atendida",
            Asistencias.fecha_llamada >= desde,
            Asistencias.fecha_llamada <= hasta
        ).count()
    else:
        asistencias_pendientes = Asistencias.query.filter(Asistencias.estado=="pendiente").count()
        asistencias_atendidas = Asistencias.query.filter(Asistencias.estado=="atendida").count()
    return {"asistencias_atendidas":asistencias_atendidas,"asistencias_pendientes":asistencias_pendientes}

def conteo_asistencias_planta(n_planta:int,desde="",hasta="") -> dict:
    """Función para devolver el número de asistencias atendidas 
    y no atendidas por planta."""
    if desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        asistencias_pendientes = Asistencias.query.join(
                Habitaciones,Asistencias.habitacion_fk==Habitaciones.numero
            ).join(
                Camas,Asistencias.cama_fk==Camas.id
            ).filter(
            Habitaciones.planta_fk==n_planta,
            Asistencias.estado=="pendiente",
            Asistencias.fecha_llamada >= desde,
            Asistencias.fecha_llamada <= hasta,
        ).count()
        asistencias_atendidas = Asistencias.query.join(
                Habitaciones,Asistencias.habitacion_fk==Habitaciones.numero
            ).filter(
            Habitaciones.planta_fk==n_planta,
            Asistencias.estado=="atendida",
            Asistencias.fecha_llamada >= desde,
            Asistencias.fecha_llamada < hasta,
        ).count()
    else:
        asistencias_pendientes = Asistencias.query.join(
                Habitaciones,Asistencias.habitacion_fk==Habitaciones.numero
            ).join(Camas).filter(
            Habitaciones.planta_fk==n_planta,
            Asistencias.estado=="pendiente"
        ).count()
        asistencias_atendidas = Asistencias.query.join(
                Habitaciones,Asistencias.habitacion_fk==Habitaciones.numero
            ).filter(
            Habitaciones.planta_fk==n_planta,
            Asistencias.estado=="atendida"
        ).count()
    return {"asistencias_atendidas":asistencias_atendidas,"asistencias_pendientes":asistencias_pendientes}

def obtener_historico(desde="",hasta="") -> list[dict]:
    """Función para obtener asistencias por mes y año."""
    if desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        asistencias_historico = db.session.query(
            extract('year',Asistencias.fecha_llamada).label('anio'),
            extract('month',Asistencias.fecha_llamada).label('mes'),
            func.count(Asistencias.id).label("conteo_asistencias")
        ).filter(
            Asistencias.fecha_llamada >= desde, Asistencias.fecha_llamada <= hasta,
        ).group_by('mes','anio').order_by('mes','anio').all()
    else:    
        asistencias_historico = db.session.query(
            extract('year',Asistencias.fecha_llamada).label('anio'),
            extract('month',Asistencias.fecha_llamada).label('mes'),
            func.count(Asistencias.id).label("conteo_asistencias")
        ).group_by('mes','anio').order_by(extract('year',Asistencias.fecha_llamada).asc(),extract('month',Asistencias.fecha_llamada).asc()).all()
    resultado_dict = [
        {
            "anio":asistencia[0],
            "mes":asistencia[1],
            "total_asistencias":asistencia[2]
        } for asistencia in asistencias_historico
    ]
    return resultado_dict

def obtener_conteo_asistencias_planta(desde="",hasta="") -> dict:
    """Función para devolver el número de asistencias atendidas y 
    no atendidas por planta."""
    if desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        asistencias_por_planta = db.session.query(
            Habitaciones.planta_fk,
            func.count(Asistencias.id).label("total_asistencias")
        ).join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero).filter(
            Asistencias.estado == "atendida",
            Asistencias.fecha_llamada >= desde,
            Asistencias.fecha_llamada <= hasta
        ).group_by(Habitaciones.planta_fk).all()
        asistencias_atendidas_dict = [
            {
            "planta": asistencia[0],
            "total_asistencias": asistencia[1]
            } for asistencia in asistencias_por_planta
        ]
    else:
        asistencias_por_planta = db.session.query(
            Habitaciones.planta_fk,
            func.count(Asistencias.id).label("total_asistencias")
        ).join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero).filter(
            Asistencias.estado=="atendida"
        ).group_by(Habitaciones.planta_fk).all()

        asistencias_atendidas_dict = [
            {
                "planta": asistencia[0],
                "total_asistencias": asistencia[1]
            } for asistencia in asistencias_por_planta
        ]
    return {"asistencias_atendidas":asistencias_atendidas_dict}

def obtener_llamados_habitaciones(desde="",hasta="") -> list[Asistencias]:
    """Función para obtener las 10 habitaciones con más llamados."""
    if desde != "" and hasta != "":
        desde = datetime.strptime(desde,"%Y-%m-%d")
        hasta = datetime.strptime(hasta,"%Y-%m-%d")
        habitaciones = db.session.query(
            Asistencias.habitacion_fk,
            func.count(Asistencias.id).label("conteo_llamadas")
        ).filter(
            Asistencias.fecha_llamada >= desde,
            Asistencias.fecha_llamada <= hasta
        ).group_by(Asistencias.habitacion_fk).order_by(func.count(Asistencias.id).desc()).limit(10).all()
    else:
        habitaciones = db.session.query(
            Asistencias.habitacion_fk,
            func.count(Asistencias.id).label("conteo_llamadas")
        ).group_by(Asistencias.habitacion_fk).order_by(func.count(Asistencias.id).desc()).limit(10).all()
    return habitaciones

def calcular_porcentaje_asistencias_totales(desde="",hasta="") -> dict:
    """Función para calcular el porcentaje de asistencias atendidas en 
    comparación con el de no atendidas."""
    asistencias_totales = conteo_asistencias(desde,hasta)
    total_asistencias = asistencias_totales["asistencias_atendidas"] + asistencias_totales["asistencias_pendientes"]
    if total_asistencias != 0:
        porcentaje_atendidas = asistencias_totales["asistencias_atendidas"] / total_asistencias * 100
        porcentaje_no_atendidas = asistencias_totales["asistencias_pendientes"] / total_asistencias * 100
    else:
        porcentaje_atendidas = 0
        porcentaje_no_atendidas = 0
    return {"porcentaje_atendidas":porcentaje_atendidas,"porcentaje_no_atendidas":porcentaje_no_atendidas}

def crearUsuario(user:str,password:str) -> bool:
    """Función para crear un usuario con hash."""
    try:
        user = User(user=user,password=password)
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        print("Error al crear usuario: ",e)
        return False

def login(user:str,password:str) -> User:
    """Función para consultar e iniciar sesión."""
    try:
        user_db = User.query.filter(User.user == user).first()
        return user_db if user_db is not None and user_db.check_password(user_db.password,password) else None
    except Exception as e:
        print("Error al iniciar sesión: ",e)
        return None
    
def getUser(id:int) -> User:
    """Función para consultar un usuario por su Id."""
    try:
        user_db = User.query.filter(User.id == id).first()
        return user_db if user_db is not None else None
    except Exception as e:
        print("Error al consultar usuario: ",e)
        return None
    
def getAsistente(usuario:str,codigo:str) -> Asistentes:
    """Función para consultar un asistente por su código y usuario."""
    try:
        asistente = Asistentes.query.filter(Asistentes.nombre==usuario,Asistentes.codigo == codigo).first()
        return asistente if asistente is not None else None
    except Exception as e:
        print("Error al obtener asistente: ",e)
        return None
    
def crear_asistencia(habitacion:int,nombre_cama:str) -> Asistencias:
    """Función para crear una asistencia con el número de habitación e Id de cama."""
    try:
        cama = Camas.query.filter(Camas.habitacion_fk == habitacion,Camas.nombre == nombre_cama).first()
        asistencias_pendientes = Asistencias.query.filter(
            Asistencias.habitacion_fk==habitacion,
            Asistencias.cama_fk==cama.id,
            Asistencias.estado=="pendiente"
        ).count()
        if asistencias_pendientes == 0:
            asistencia = Asistencias(habitacion_fk=habitacion,cama_fk= cama.id)
            db.session.add(asistencia)
            db.session.commit()
            return asistencia
        else:
            return False
    except Exception as e:
        print("Error al crear asistencia: ",e)
        db.session.rollback()
        return False
    
def atender_asistencia(id_asistencia:int,asistente:Asistentes) -> bool:
    """Función para asignar una asistencia específica a un asistente."""
    try:
        asistencia = Asistencias.query.join(
            Habitaciones,Habitaciones.numero == Asistencias.habitacion_fk
        ).filter(
            Asistencias.id==id_asistencia,
            Asistencias.estado=="pendiente",
            Habitaciones.planta_fk == asistente.planta_fk
        ).first()
        if asistencia != None:
            asistencia.asistente_fk = asistente.dni
            asistencia.estado = "leída"
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print("Error al asignar asistencia: ",e)
        db.session.rollback()
        return False
    
def presencia_asistencia(habitacion:int,nombre_cama:str) -> bool:
    """Función para asignar la hora de la presencia del asistente."""
    try:
        cama = Camas.query.filter(Camas.habitacion_fk == habitacion,Camas.nombre == nombre_cama).first()
        asistencia = Asistencias.query.filter(
            Asistencias.habitacion_fk==habitacion,
            Asistencias.cama_fk==cama.id,
            Asistencias.estado=="leída"
        ).first()
        if asistencia != None:
            asistencia.fecha_presencia = datetime.now()
            asistencia.estado = "atendida"
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print("Error al asignar presencia: ",e)
        db.session.rollback()
        return False
    
def registrar_dispositivo(tipo:str,ip:str,puerto:int,habitacion:int,
                          cama_id:int) -> bool:
    """Función para registrar un dispositivo como relé o pulsador."""
    try:
        dispositivo = Dispositivos(tipo,ip,puerto,habitacion,cama_id)
        db.session.add(dispositivo)
        db.session.commit()
        return True
    except Exception as e:
        print("Error: ",e)
        db.session.rollback()

def consultar_rele_cama(habitacion:int,cama:int|str) -> Dispositivos:
    """Función para consultar un relé asociado a una cama y 
    una habitación específica."""
    try:
        if isinstance(cama,str):
            cama = Camas.query.filter(Camas.habitacion_fk==habitacion,Camas.nombre==cama).first()
            dispositivo = Dispositivos.query.filter(Dispositivos.habitacion_fk==habitacion,Dispositivos.cama_fk==cama.id).first()
        else:
            dispositivo = Dispositivos.query.filter(Dispositivos.habitacion_fk==habitacion,Dispositivos.cama_fk==cama).first()
        return dispositivo
    except Exception as e:
        print("Error: ",e)

def obtener_asistencia(id:int) -> Asistencias:
    """Función que devuelve una asistencia por su Id."""
    try:
        asistencia = Asistencias.query.filter(Asistencias.id==id).first()
        return asistencia
    except Exception as e:        
        print("Error: ",e)
        return None
    
def actualizar_estado_asistente(asistente:Asistencias,estado:bool) -> bool:
    """Función para actualizar el estado del asistente entre inactivo y activo."""
    actualizado = False
    try:
        asistente.activo = estado
        db.session.commit()
        actualizado = True
    except Exception as e:
        print("Error al cambiar estado: ",e)
        db.session.rollback()
    
    return actualizado

def obtener_asistencias_filtros(filtros:dict) -> list[Asistencias]:
    """Función para obtener asistencias según filtros de fecha, 
    asistente, habitación y planta."""
    try:
        asistencias = None
        if filtros.get("fechas") != None and filtros.get("asistente") != None and \
            filtros.get("habitacion") != None and filtros.get("planta") != None:
            desde = datetime.strptime(filtros["fechas"]["desde"],"%Y-%m-%d")
            hasta = datetime.strptime(filtros["fechas"]["hasta"],"%Y-%m-%d")
            print(filtros)
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"],
                    Asistencias.fecha_llamada >= desde, 
                    Asistencias.fecha_llamada <= hasta,
                    Asistencias.asistente_fk == filtros["asistente"],
                    Asistencias.habitacion_fk == filtros["habitacion"]).all()
        elif filtros.get("fechas") != None and filtros.get("asistente") != None and \
            filtros.get("habitacion") == None and filtros.get("planta") != None:
            desde = datetime.strptime(filtros["fechas"]["desde"],"%Y-%m-%d")
            hasta = datetime.strptime(filtros["fechas"]["hasta"],"%Y-%m-%d")
            print(filtros)
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"],
                    Asistencias.fecha_llamada >= desde, 
                    Asistencias.fecha_llamada <= hasta,
                    Asistencias.asistente_fk == filtros["asistente"]).all()
        elif filtros.get("fechas") != None and filtros.get("asistente") == None and \
            filtros.get("habitacion") == None and filtros.get("planta") != None:
            desde = datetime.strptime(filtros["fechas"]["desde"],"%Y-%m-%d")
            hasta = datetime.strptime(filtros["fechas"]["hasta"],"%Y-%m-%d")
            print(filtros)
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"],
                    Asistencias.fecha_llamada >= desde, 
                    Asistencias.fecha_llamada <= hasta) \
            .all()
        elif filtros.get("fechas") != None and filtros.get("asistente") == None and \
            filtros.get("habitacion") == None and filtros.get("planta") == None:
            print(filtros)
            desde = datetime.strptime(filtros["fechas"]["desde"],"%Y-%m-%d")
            hasta = datetime.strptime(filtros["fechas"]["hasta"],"%Y-%m-%d")
            asistencias = Asistencias.query.filter(
                Asistencias.fecha_llamada >= desde, 
                Asistencias.fecha_llamada <= hasta,
            ) 
        elif filtros.get("fechas") == None and filtros.get("asistente") != None and \
            filtros.get("habitacion") == None and filtros.get("planta") == None:
            print(filtros)
            asistencias = Asistencias.query.filter(
                Asistencias.asistente_fk == filtros["asistente"],
            ) 
        elif filtros.get("fechas") != None and filtros.get("asistente") != None and \
            filtros.get("habitacion") == None and filtros.get("planta") == None:
            print(filtros)
            desde = datetime.strptime(filtros["fechas"]["desde"],"%Y-%m-%d")
            hasta = datetime.strptime(filtros["fechas"]["hasta"],"%Y-%m-%d")
            asistencias = Asistencias.query.filter(
                Asistencias.fecha_llamada >= desde, 
                Asistencias.fecha_llamada <= hasta,
                Asistencias.asistente_fk == filtros["asistente"]
            ) 
        elif filtros.get("fechas") == None and filtros.get("asistente") != None and \
            filtros.get("habitacion") == None and filtros.get("planta") != None:
            print(filtros)
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"],
                    Asistencias.asistente_fk == filtros["asistente"]).all()
        elif filtros.get("fechas") == None and filtros.get("asistente") != None and \
            filtros.get("habitacion") != None and filtros.get("planta") != None:
            print(filtros)
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"],
                    Asistencias.asistente_fk == filtros["asistente"],
                    Asistencias.habitacion_fk == filtros["habitacion"]).all()
            
        elif filtros.get("fechas") == None and filtros.get("asistente") == None and \
            filtros.get("habitacion") != None and filtros.get("planta") == None:
            asistencias = Asistencias.query.filter(
                Asistencias.habitacion_fk == filtros["habitacion"]
            ) 
        elif filtros.get("fechas") == None and filtros.get("asistente") != None and \
            filtros.get("habitacion") != None and filtros.get("planta") == None:
            asistencias = Asistencias.query.filter(
                Asistencias.habitacion_fk == filtros["habitacion"],
                Asistencias.asistente_fk == filtros["asistente"]
            ) 
        elif filtros.get("fechas") != None and filtros.get("asistente") == None and \
            filtros.get("habitacion") != None and filtros.get("planta") == None:
            desde = datetime.strptime(filtros["fechas"]["desde"],"%Y-%m-%d")
            hasta = datetime.strptime(filtros["fechas"]["hasta"],"%Y-%m-%d")
            asistencias = Asistencias.query.filter(
                Asistencias.fecha_llamada >= desde, 
                Asistencias.fecha_llamada <= hasta,
                Asistencias.habitacion_fk == filtros["habitacion"]
            ) 
        elif filtros.get("fechas") == None and filtros.get("asistente") == None and \
            filtros.get("habitacion") != None and filtros.get("planta") != None:
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"],
                    Asistencias.habitacion_fk == filtros["habitacion"]).all()
        elif filtros.get("fechas") == None and filtros.get("asistente") == None and \
            filtros.get("habitacion") == None and filtros.get("planta") != None:
            asistencias = db.session.query(Asistencias) \
            .join(Habitaciones, Asistencias.habitacion_fk == Habitaciones.numero) \
            .filter(Habitaciones.planta_fk == filtros["planta"]).all()
        else:
            asistencias = obtener_asistencias()
        return asistencias
    except Exception as e:
        print("Error al obtener asistencias: ",e)

def obtener_habitaciones() -> list[Habitaciones]:
    """Función para obtener todas las habitaciones."""
    try:
        habitaciones = Habitaciones.query.all()
        return habitaciones
    except Exception as e:
        print("Error al obtener habitaciones: ",e)

def obtener_camas() -> list[Camas]:
    """Función para obtener todas las camas."""
    try:
        camas_habitacion = Camas.query.join(
            Habitaciones, Camas.habitacion_fk == Habitaciones.numero
        ).all()
        return camas_habitacion
    except Exception as e:
        print("Error al obtener camas: ",e)
    

def obtener_camas_habitacion(n_habitacion:int) -> list[Camas]:
    """Función para obtener todas las camas 
    asociadas a una habitación."""
    try:
        camas = Camas.query.join(
            Habitaciones, Camas.habitacion_fk == Habitaciones.numero
        ).filter(Habitaciones.numero == n_habitacion).all()
        return camas
    except Exception as e:
        print("Error al obtener camas: ",e)
    


def obtener_dispositivos() -> list[dict]:
    """Función para obtener todos los dispositivos."""
    try:
        dispositivos = Dispositivos.query.join(
            Camas,Dispositivos.cama_fk == Camas.id
        ).add_columns(
            Camas.nombre.label("nombre")
        ).all()
        dispositivos_dict = [{
                "id":dispositivo[0].id,
                "tipo":dispositivo[0].tipo,
                "ip":dispositivo[0].ip,
                "puerto":dispositivo[0].puerto,
                "habitacion_fk":dispositivo[0].habitacion_fk,
                "cama_fk":dispositivo[0].cama_fk,
                "nombre_cama":dispositivo[1].upper(),
                "fecha_registro":dispositivo[0].fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
            } for dispositivo in dispositivos]
        return dispositivos_dict
    except Exception as e:
        print("Error al obtener dispositivos: ",e)
        return None
    
def actualizar_dispositvos(dispositivos:list[dict]) -> bool:
    """Función para actualizar datos de múltiples dispositivos."""
    try:
        for dispositivo in dispositivos:
            dispositivo_db = Dispositivos.query.filter(Dispositivos.id==dispositivo["id"]).first()
            dispositivo_db.tipo = dispositivo["tipo"]
            dispositivo_db.ip = dispositivo["ip"]
            dispositivo_db.puerto = dispositivo["puerto"]
            dispositivo_db.habitacion_fk = dispositivo["habitacion"]
            dispositivo_db.cama_fk = dispositivo["cama"]
        db.session.commit()
        return True
    except Exception as e:
        print("Error al actualizar dispositivos: ",e)
        return False
    
def eliminar_dispositivos(ids:list[int]) -> bool:
    """Función para eliminar dispositivo por su Id."""
    try:
        for id in ids:
            dispositivo = Dispositivos.query.filter(Dispositivos.id==id).first()
            if dispositivo is not None:
                db.session.delete(dispositivo)
                db.session.commit()
        return True
    except Exception as e:
        print("Error al eliminar dispositivo: ",e)
        return False