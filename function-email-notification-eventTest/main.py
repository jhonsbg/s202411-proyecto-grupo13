# import base64
# import json

# # from ..function-email-notification.main import pubsub_trigger


# # Datos que quieres simular que son enviados en tu mensaje de Pub/Sub
# message_data = {
#     'to': 'jhonsbg@gmail.com',
#     'subject': 'Prueba de Envío',
#     'body': 'Este es el cuerpo del mensaje.'
# }

# # Codifica tus datos como un mensaje de Pub/Sub
# simulated_pubsub_message = base64.b64encode(json.dumps(message_data).encode("utf-8")).decode("utf-8")

# # Crea el objeto de evento simulado
# event = {
#     'data': simulated_pubsub_message
# }

# # Contexto simulado (puedes dejarlo vacío o simular valores según necesites)
# context = {}

# # pubsub_trigger(event, context)

import json
import os
from google.cloud import pubsub_v1
from flask import jsonify

# Se leen las variables de entorno especificadas
# project_id = os.environ.get('PROJECT_ID', '')
project_id = 'myproject-8ceb8'
# email_topic = os.environ.get('EMAIL_TOPIC', '')
email_topic = 'send-email'

# Instancia del cliente de comunicación  Pub/Sub
publisher = pubsub_v1.PublisherClient()

def peticion_enviar_email(request):
    body = {
        'to': 'jhonsbg@gmail.com',
        'subject': 'Prueba de Envío',
        'body': 'Este es el cuerpo del mensaje.'
    }

    print("Project ID:", project_id)
    print("Email topic:", email_topic)
    # Construye el nombre del tema a la que se realizará la publicación del mensaje
    topic_path = publisher.topic_path(project_id, email_topic)
    # Construcción del mensaje que se enviará
    message_json = json.dumps(body)
    message_bytes = message_json.encode('utf-8')
    # Se realiza la publicación del mensaje en el topico
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return jsonify({'message': 'Email enviado'}), 200
    except Exception as e:
        print('Error al momento de publicar')
        print(e)
        return jsonify({'error': 'Error al momento de enviar', 'details': str(e)}), 500