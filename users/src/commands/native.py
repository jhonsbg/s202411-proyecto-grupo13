from ..errors.errors import NotFoundException
from .base_command import BaseCommannd
import requests
import os
import datetime
import random
import string

class Native(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    webhook = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'http://localhost:3000'
    webhook = webhook + '/users'
    letraTran = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    numTran = int(datetime.datetime.utcnow().timestamp())
    transactionId = f'{letraTran}_{numTran}'
    verification_data = {
      "user": {
          "email": self.json_data["email"],  
          "dni": self.json_data["dni"],  
          "fullName": self.json_data["username"],
          "phone": self.json_data["phoneNumber"]
      },
      "transactionIdentifier": transactionId,
      "userIdentifier": self.json_data["dni"],
      "userWebhook": webhook
    }
    host = os.environ['NATIVE_PATH'] if 'NATIVE_PATH' in os.environ else 'http://192.168.0.11:3010'
    token = os.environ['SECRET_TOKEN'] if 'SECRET_TOKEN' in os.environ else 'qwerty'
    try:
      response = requests.post(
          f'{host}/native/verify',
          headers={
              'Authorization': f'{token}'
          },
          json=verification_data
      )
    except: 
       print('No ingresó al servicio de truenative')
       raise NotFoundException
    
    if response.status_code == 201:
        return response.status_code
    else: 
        raise NotFoundException
    