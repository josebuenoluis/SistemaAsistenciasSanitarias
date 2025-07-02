#!/bin/bash
echo "Iniciando Nginx"
service nginx start

echo "Activando entorno virtual..."
source env/bin/activate

echo "Creando tablas si no existen..."
sleep 10 && python3 index.py

echo "Iniciando gunicorn..."
exec gunicorn --workers 4 --bind 0.0.0.0:8000 app:app