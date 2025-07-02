from app import app
from models.db import db

with app.app_context():
    
    db.create_all()
