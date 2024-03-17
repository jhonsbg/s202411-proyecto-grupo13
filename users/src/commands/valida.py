from ..errors.errors import BadRequestException
from .base_command import BaseCommannd
from ..models import db, User
import hashlib
import os
from datetime import datetime, timezone, timedelta
from google.cloud import pubsub_v1
import json

# Se leen las variables de entorno especificadas
projec_id = os.environ.get('PROJECT_ID', '')
email_topic = os.environ.get('EMAIL_TOPIC', '')

# Instancia del cliente de comunicación  Pub/Sub
publisher = pubsub_v1.PublisherClient()

class Valida(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    #genera fecha de modificación
    fecha= datetime.now(timezone.utc)
    zona = timezone(timedelta(hours=-5))
    fechazona = fecha.astimezone(zona)
    formato = "%Y-%m-%d %H:%M:%S.%f %z"
    fupdate = fechazona.strftime(formato)
    token = os.environ['SECRET_TOKEN'] if 'SECRET_TOKEN' in os.environ else 'qwerty'
    ruv = self.json_data["RUV"]
    score = self.json_data["score"]
    #validación token
    validaToken = f"{token}:{ruv}:{score}"
    sha_token = hashlib.sha256(validaToken.encode()).hexdigest()
    if sha_token == self.json_data["verifyToken"]:
      existing_user = User.query.filter_by(dni=self.json_data["userIdentifier"]).first() 
      existing_user.status = self.json_data["status"]
      existing_user.updateAt = fupdate
      db.session.commit()
      print('sending email...')
      send_message(email_topic, {
          "to": existing_user.email,
          "subject": f"Verificación de usuario {existing_user.fullName}",
          "body": f"La solicitud de verificación del usuario {existing_user.fullName} se encuentra en estado {existing_user.status.name}"
      })
      return 'OK'
    else:
      raise BadRequestException()
    
  

def send_message(topic, message):
    topic_path = publisher.topic_path(projec_id, topic)
    message_json =json.dumps(message)
    message_bytes = message_json.encode('utf-8')
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result() 
    except Exception as e:
        print('Error al momento de publicar')
        print(e)

