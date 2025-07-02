import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

def enviarCorreo(email_destinatario:str,archivo_bytes:BytesIO,nombre_archivo:str) -> None:

    textoHtml = f"""
    <html>
        <body>
            <h2>Hola, te adjunto el archivo solicitado. Saludos, GrupoVital.</h2>        
        </body>
    </html>"""

    enviado_por = ''
    password = ''

    mensaje = MIMEMultipart()
    mensaje['From'] = enviado_por
    mensaje['To'] = email_destinatario
    mensaje['Subject'] = f'Archivo de asistencias solicitado.'  

    mensaje.attach(MIMEText(textoHtml,'html'))

    mime_base = MIMEBase('application','octet-stream')
    mime_base.set_payload(archivo_bytes.read())
    encoders.encode_base64(mime_base)
    mime_base.add_header('Content-Disposition',f'attachment; filename={nombre_archivo}')
    mensaje.attach(mime_base)

    try:
        servidor = smtplib.SMTP('mail.gmx.es',587)
        servidor.starttls()
        servidor.login(enviado_por,password)
        servidor.sendmail(enviado_por,email_destinatario,mensaje.as_string())
        servidor.quit()
    except Exception as error:
        print(f"Error al enviar el correo: {error}")
