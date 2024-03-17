from .autorizacion import Autorizacion
from .base_command import BaseCommand
from ..models.card import db, Card, StatusCardEnum
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
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        print(self.json_data['RUV'])
        card = Card.query.filter_by(ruv=self.json_data['RUV']).first()
        
        if card is None:
            raise NotFoundSecretToken()
        
        user = Autorizacion(f'Bearer {card.userId}').execute()
        if user is None:
            raise NotFoundSecretToken()
        
        card.updatedAt = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        card.status = self.json_data['status']

        print(card.status)
        db.session.commit()

        send_message(email_topic, {
            'to': user.email,
            'subject': f'Verificación de tarjeta de {user.fullName}',
            'body': f'La solicitud de verificación de la tarjeta {card.lastFourDigits} se encuentra en estado {card.status}'
        })

        print('enviado')
        
        
        



    