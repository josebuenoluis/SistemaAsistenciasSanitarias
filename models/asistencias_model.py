from .db import db
from datetime import datetime


class Asistencias(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    habitacion_fk = db.Column(db.Integer,db.ForeignKey("habitaciones.numero"))
    cama_fk = db.Column(db.Integer,db.ForeignKey("camas.id"))
    fecha_llamada = db.Column(db.DateTime,default=datetime.now)
    fecha_presencia = db.Column(db.DateTime,nullable=True)
    asistente_fk = db.Column(db.String(9),db.ForeignKey("asistentes.dni"),nullable=True)
    estado = db.Column(db.Enum("pendiente","leída","atendida"),default="pendiente")
    
    def to_dict(self) -> dict:
        """Método para convertir el modelo a diccionario."""
        return {
            "id":self.id,
            "habitacion_fk":self.habitacion_fk,
            "cama_fk":self.cama_fk,
            "fecha_llamada":self.fecha_llamada.strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_presencia":self.fecha_presencia.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_presencia != None else self.fecha_presencia,
            "asistente_fk":self.asistente_fk,
            "estado":self.estado
        }