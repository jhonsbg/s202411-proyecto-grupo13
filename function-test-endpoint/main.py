import json
import os
from google.cloud import pubsub_v1

# Se leen las variables de entorno especificadas
projec_id = os.environ.get('PROJECT_ID', '')
tema_publicacion = os.environ.get('TOPIC', '')

# Instancia del cliente de comunicación  Pub/Sub
publisher = pubsub_v1.PublisherClient()

def enviar_mensaje(request):
    """Definición de la función para realizar una llamada de auxilio. 
    La función realiza la publicación de un mensaje en el tema especificado
    
    Args:
        request (flask.Request): Objeto con la información de la petición.
    Returns:
        Información de la tarea creada
    """
    # Construye el nombre del tema a la que se realizará la publicación del mensaje
    topic_path = publisher.topic_path(projec_id, tema_publicacion)
    # Construcción del mensaje que se enviará
    message_json = json.dumps({
        'data': request.get_json(silent=True),
    })
    message_bytes = message_json.encode('utf-8')
    # Se realiza la publicación del mensaje en el topico
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return 'Tarjeta Creada...'
    except Exception as e:
        print('Error al momento de publicar')
        print(e)
        return e
