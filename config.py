
class Config:
    """Configuracion base"""
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:jose@db:3306/asistencia_sanitaria"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "12345678"
    JWT_KEY = "D5*F?_1-d$f*1"