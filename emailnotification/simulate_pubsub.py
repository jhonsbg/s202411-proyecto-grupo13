import base64
import json

from notify.main import pubsub_trigger


# Datos que quieres simular que son enviados en tu mensaje de Pub/Sub
message_data = {
    'to': 'jhonsbg@gmail.com',
    'subject': 'Prueba de Envío',
    'body': 'Este es el cuerpo del mensaje.'
}

# Codifica tus datos como un mensaje de Pub/Sub
simulated_pubsub_message = base64.b64encode(json.dumps(message_data).encode("utf-8")).decode("utf-8")

# Crea el objeto de evento simulado
event = {
    'data': simulated_pubsub_message
}

# Contexto simulado (puedes dejarlo vacío o simular valores según necesites)
context = {}

pubsub_trigger(event, context)
