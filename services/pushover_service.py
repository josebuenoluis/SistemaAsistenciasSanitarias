import urllib
import urllib.request
import json

# Guardar en variables de entorno
USER_KEY = ""
API_KEY = ""
URL = ""


def enviar_mensaje(data:dict) -> bool:
    """Función para enviar un mensaje mediante la API de PushOver."""
    data_json = json.dumps(data).encode("utf-8")
    enviado = False
    req = urllib.request.Request(
    URL,
    data=data_json,
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode()
            enviado = True
    except urllib.error.HTTPError as e:
        print("Error en la petición:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("Error de conexión:", e.reason)
    return enviado
