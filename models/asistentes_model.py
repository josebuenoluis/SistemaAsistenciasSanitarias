from .db import db

class Asistentes(db.Model):
    dni = db.Column(db.String(9),unique=True,primary_key=True)
    nombre = db.Column(db.String(45))
    telefono = db.Column(db.Integer,unique=True)
    codigo = db.Column(db.String(6),unique=True)
    planta_fk = db.Column(db.Integer)
    activo = db.Column(db.Boolean)

    def __init__(self,dni,nombre,telefono,codigo,planta_fk) -> None:
        self.dni = dni
        self.nombre = nombre
        self.telefono = telefono
        self.codigo = codigo
        self.planta_fk = planta_fk
        self.activo = False

    def to_dict(self) -> dict:
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "codigo": self.codigo,
            "planta_fk": self.planta_fk,
            "activo": self.activo
        }