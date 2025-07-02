# 🏥 Sistema de Asistencias Sanitarias

Aplicación web para la gestión de asistencias sanitarias en centros de salud, que facilita el registro, seguimiento y administración de pacientes y servicios médicos.

---

## 🚀 Funcionalidades

- Gestión de dos tipos de usuarios: administradores y asistentes.
- Registro y gestión de pacientes.
- Control y seguimiento de asistencias médicas.
- Sistema de atención por pulsador:  
  - Cuando un paciente presiona un pulsador, se encienden luces que indican la atención requerida.  
  - El asistente (enfermero) confirma su presencia pulsando un botón, y el evento se registra en la base de datos.  
- Administración de servicios y personal sanitario.
- Reportes y análisis para que los administradores puedan evaluar las asistencias.

---

## 🛠️ Tecnologías utilizadas

- Backend: Flask (Python) con Jinja2 para templates.
- Frontend: Bootstrap para diseño responsivo.
- ORM: SQLAlchemy para la gestión de la base de datos MariaDB.
- Servidor WSGI: Gunicorn.
- Servidor web: Nginx (proxy reverso).
- Base de datos: MariaDB.
- Sistema operativo: Ubuntu.
- Contenedores: Docker para toda la aplicación.

