import base64
import requests
import os
import json

def verifier(event, context):
    """Definición de la función invocada por el servicio Pub/Sub. 
    La función verifica el proceso de validación de una tarjeta de credito en TrueNative
    
    Args:
        event (dic): Objeto con la información de la petición.
        context (dic): Información del evento generado
    Returns:
        Respuesta en caso de exito
    """
    json_data = json.loads(base64.b64decode(event['data']).decode())
    card_ruv = json_data['data']['RUV']

    host = os.environ['INGRESS_PATH']
    secret_token = os.environ['SECRET_TOKEN']

    response = requests.get(
        f'http://{host}/native/cards/{card_ruv}',
        headers={
            'Authorization': f'Bearer {secret_token}'
        }
    )

    if response.status_code == 200:
        response_json = response.json()
        response = requests.patch(
            f'http://{host}/credit-cards',
            data=response_json
            # {
            #     "RUV": "cXdlcnR5MTIzNDU2MzplYWUyNGI5NTM5MWFhODQyYmYwYTIxODUzYTIzNThiMjJiMWQ3ZTdlMDIzZmY0ODkyNTZjNGE2MmM3NTZiZjU4",
            #     "createdAt": "Sun, 10 Mar 2024 22:56:20 GMT",
            #     "status": "APROBADA",
            #     "transactionIdentifier": "qwerty1234563"
            # }
        )
        return 'OK'
    else:
        raise RuntimeError()