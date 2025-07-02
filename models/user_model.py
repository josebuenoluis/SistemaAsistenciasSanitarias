from .db import db
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user = db.Column(db.String(45),unique=True)
    password = db.Column(db.String(128))

    def __init__(self,user:str,password:str):
        self.user = user
        self.password = generate_password_hash(password,method="pbkdf2:sha256:600000")

    @classmethod
    def check_password(self,hashed_password:str,password:str):
        return check_password_hash(hashed_password,password)