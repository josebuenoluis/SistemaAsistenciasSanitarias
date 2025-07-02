from .db import db
from datetime import datetime


class Dispositivos(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    tipo = db.Column(db.Enum('pulsador', 'rele'), nullable=False)
    ip = db.Column(db.String(15),nullable=False)
    puerto = db.Column(db.Integer,default=80)
    habitacion_fk = db.Column(db.Integer,db.ForeignKey("habitaciones.numero"))
    cama_fk = db.Column(db.Integer,db.ForeignKey("camas.id"))
    fecha_registro = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,tipo:str,ip:str,puerto:int,habitacion:int,cama:int):
        self.tipo = tipo
        self.ip = ip
        self.puerto = puerto
        self.habitacion_fk = habitacion
        self.cama_fk = cama
        
    def to_dict(self):
        return {
            "id":self.id,
            "tipo":self.tipo,
            "ip":self.ip,
            "puerto":self.puerto,
            "habitacion":self.habitacion_fk,
            "cama":self.cama_fk,
            "fecha_registro":self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
        }