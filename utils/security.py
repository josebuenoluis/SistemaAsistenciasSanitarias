import jwt
import datetime
from models.asistentes_model import Asistentes
import pytz
from config import Config
from services import mariadb_service as db_service

class Security():
    tz = pytz.timezone("America/Lima")
    secret = Config.JWT_KEY
    
    @classmethod
    def generate_token(self,authenticated_user:Asistentes) -> str:
        """Método para generar JWT, mediante el módulo jwt y 
        una instancia del modelo Asistentes."""
        payload = {
            'iat':datetime.datetime.now(tz=self.tz),
            # 'exp':datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=10),
            'username':authenticated_user.nombre,
            "codigo":authenticated_user.codigo
        }
        return jwt.encode(payload,self.secret,algorithm="HS256")
    
    @classmethod
    def verify_token(self,headers:dict) -> bool:
        if 'Authorization' in headers.keys():
            authorization = headers["Authorization"]
            encoded_token = authorization.split(" ")[1]
            try:
                payload = jwt.decode(encoded_token,self.secret,algorithms=["HS256"])
                return True 
            except (jwt.ExpiredSignatureError,jwt.InvalidSignatureError,jwt.InvalidTokenError):
                return False
        return False
    
    @classmethod
    def verify_token_cookie(self,cookie_token:str) -> bool:
        try:
            payload = jwt.decode(cookie_token,self.secret,algorithms=["HS256"]) 
            return True 
        except (jwt.ExpiredSignatureError,jwt.InvalidSignatureError,jwt.InvalidTokenError):
            return False
        
    @classmethod
    def decode_token_cookie(self,cookie_token:str):
        try:
            payload = jwt.decode(cookie_token,self.secret,algorithms=["HS256"]) 
            return payload 
        except (jwt.ExpiredSignatureError,jwt.InvalidSignatureError,jwt.InvalidTokenError):
            return False