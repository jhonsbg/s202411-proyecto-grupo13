import base64
import json

from .utilidades import send_email


def pubsub_trigger(event, context):
    if'data' in event:
        message_data = base64.b64decode(event['data']).decode('utf-8')
        message = json.loads(message_data)

        success = send_email(message['to'], message['subject'], message['body'])

        if success:
            print("Email enviado con éxito")
        else:
            print("Error al enviar el email")
    else:
        print("No data found in event")