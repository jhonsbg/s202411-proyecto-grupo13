import uuid
from .base_command import BaseCommand
from ..models.card import Card, db, StatusEnum
from ..errors.errors import BadRequestException, InvalidSecretToken, NotFoundSecretToken, ExistentRequestCard, ExpiredCard
from flask import request, jsonify
# from google.cloud import pubsub_v1
from datetime import datetime
import os
import json
import requests

# Se leen las variables de entorno especificadas
# projec_id = os.environ.get('PROJECT_ID', '')
# card_topic = os.environ.get('CARDS_TOPIC', '')
# email_topic = os.environ.get('EMAIL_TOPIC', '')

# Instancia del cliente de comunicación  Pub/Sub
# publisher = pubsub_v1.PublisherClient()

class Create(BaseCommand):
    def __init__(self, json_data, token, user_id):
        self.json_data = json_data
        self.token = token
        self.user_id = user_id

    def execute(self):
        host_native = os.environ['TRUENATIVE_PATH'] if 'TRUENATIVE_PATH' in os.environ else 'http://localhost:3010'
        secret_token = os.environ['SECRET_TOKEN']
        print(secret_token)
        #si la fecha de la tarjeta ya está vencida
        if 'expirationDate' in self.json_data and datetime.now() > datetime.strptime(self.json_data['expirationDate'], "%y/%m"):
            raise ExpiredCard() 
        try:
            #llamado a truenative
            reponse = requests.post(
                f'{host_native}/native/cards',
                headers={
                    'Authorization': f'{secret_token}'
                },
                #armar el json para truenative
                json={
                    "card": {
                        "cardNumber": self.json_data['cardNumber'],
                        "cvv": self.json_data['cvv'],
                        "expirationDate": self.json_data['expirationDate'],
                        "cardHolderName": self.json_data['cardHolderName'],
                    },
                    "transactionIdentifier": str(uuid.uuid4())
                }
            )
        except:
            raise BadRequestException()
        
        if reponse.status_code == 401:
            raise InvalidSecretToken()
        
        if reponse.status_code == 403:
            return NotFoundSecretToken()
        
        if reponse.status_code == 409:
            return ExistentRequestCard()

        response_truenative = reponse.json()


        if response_truenative['task_status'] == "ACCEPTED":
            try:
                card = Card(
                    id = str(uuid.uuid4()), \
                    lastFourDigits = self.json_data['cardNumber'][-4:], \
                    issuer = response_truenative['issuer'], \
                    token = response_truenative['token'], \
                    status=StatusEnum.POR_VERIFICAR, \
                    ruv = response_truenative['RUV'], \
                    userId = self.user_id
                )
                db.session.add(card)
                db.session.commit()
            except: 
                raise BadRequestException()

            created_at = card.createAt

            if isinstance(created_at, tuple):
                created_at = created_at[0]

            new_card = {
                "id": card.id,
                "userId": card.userId,
                "createdAt": created_at.isoformat()
            }

            return new_card
        else:
            return response_truenative
        
    

    # def send_message(topic, body):
    #     topic_path = publisher.topic_path(projec_id, topic)
    #     message_json = json.dumps({
    #         'data': jsonify(body),
    #     })
    #     message_bytes = message_json.encode('utf-8')
    #     try:
    #         publish_future = publisher.publish(topic_path, data=message_bytes)
    #         publish_future.result() 
    #     except Exception as e:
    #         print('Error al momento de publicar')
    #         print(e)

# # Ejemplos
        
# send_message(email_topic, {
#     'to': 'hmaury1@gmail.com',
#     'subject': 'Prueba',
#     'body': 'Hola mundo'
# })

# send_message(card_topic, Card)
