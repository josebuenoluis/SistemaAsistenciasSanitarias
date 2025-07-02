from .db import db

class Plantas(db.Model):
    numero = db.Column(db.Integer,primary_key=True)
    
    def __init__(self,numero) -> None:
        self.numero = numero

    def to_dict(self) -> dict:
        return {
            "numero": self.numero
        }