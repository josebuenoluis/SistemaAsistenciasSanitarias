from .db import db

class Camas(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nombre = db.Column(db.String(20))
    habitacion_fk = db.Column(db.Integer,db.ForeignKey("habitaciones.numero"))

    def __init__(self,nombre,habitacion_fk):
        self.nombre = nombre
        self.habitacion_fk = habitacion_fk

    def to_dict(self):
        return {
            "id":self.id,
            "nombre":self.nombre,
            "habitacion_fk":self.habitacion_fk
        }