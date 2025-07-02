from .db import db

class Habitaciones(db.Model):
    __tablename__ = "habitaciones"
    numero = db.Column(db.Integer,primary_key=True)
    planta_fk = db.Column(db.Integer,db.ForeignKey("plantas.numero"))

    def __init__(self,numero,planta_fk) -> None:
        self.numero = numero
        self.planta_fk = planta_fk

    def to_dict(self):
        return {
            "numero":self.numero,
            "planta_fk":self.planta_fk
        }


