import csv
from io import TextIOWrapper,BytesIO
from services import smtp_service
def exportarCSV(data:list[dict],buffer:BytesIO) -> BytesIO:
    """Funcion para escribir los datos JSON
    en un archivo binario en memoria recibido"""
    #Obtenemos los encabezados de los datos recibidos para el CSV.
    headers = [
        header for header in data[1].keys()
    ]
    print(data)
    datosAsistencias = data[1:]
    archivoTextIo = TextIOWrapper(buffer=buffer,encoding="utf-8",newline="")
    writer = csv.DictWriter(archivoTextIo,fieldnames=headers,delimiter=data[0]["delimitador"],lineterminator="\n")
    writer.writeheader()
    writer.writerows(datosAsistencias)
    archivoTextIo.flush()
    #Separa el buffer de TextIOWrapper para que no se 
    # cierre el binario después de escribir.
    buffer_archivo = archivoTextIo.detach()
    buffer_archivo.seek(0)
    if data[0]["correo"] != "":
        buffer_correo = BytesIO(buffer_archivo.read())
        buffer_correo.seek(0)
        smtp_service.enviarCorreo(data[0]["correo"],buffer_correo,data[0]["nombre"])
        buffer_archivo.seek(0)
        
    return buffer_archivo
