from .base_command import BaseCommand
from ..models.card import Card
from ..errors.errors import NotFoundSecretToken
from flask import jsonify
from google.cloud import pubsub_v1
import os
import json
import requests
from datetime import datetime

# Se leen las variables de entorno especificadas
projec_id = os.environ.get('PROJECT_ID', '')
card_topic = os.environ.get('CARDS_TOPIC', '')
email_topic = os.environ.get('EMAIL_TOPIC', '')

# Instancia del cliente de comunicación  Pub/Sub
publisher = pubsub_v1.PublisherClient()


def send_message(topic, body):
    topic_path = publisher.topic_path(projec_id, topic)
    message_json = json.dumps({
        'data': jsonify(body),
    })
    message_bytes = message_json.encode('utf-8')
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result() 
    except Exception as e:
        print('Error al momento de publicar')
        print(e)

# # Ejemplos
        
# send_message(email_topic, {
#     'to': 'hmaury1@gmail.com',
#     'subject': 'Prueba',
#     'body': 'Hola mundo'
# })

class Update(BaseCommand):
    def __init__(self, json_data, token, user_email):
        self.json_data = json_data
        self.token = token
        self.user_email = user_email

    def execute(self):
        host = os.environ['INGRESS_PATH']
        card = Card.query.filter_by(ruv=self.json_data['RUV']).first()
        
        if card is None:
            raise NotFoundSecretToken()
        
        try:
            response = requests.patch(
                f'http://{host}/credit-cards',
                data={
                    "RUV": self.json_data['RUV'],
                    "updatedAt": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    "status": "APROBADA"
                }
            )

            send_message(email_topic, {
                'to': self.user_email,
                'subject': 'Tarjeta aprobada',
                'body': f'Tarjeta {self.json_data["RUV"]} aprobada'
            })
        except Exception as e:
            print(e)
            raise e
        
        



    