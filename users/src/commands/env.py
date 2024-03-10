from ..errors.errors import NotFoundException
from .base_command import BaseCommannd
import requests
import os
import datetime
import random
import string

class Env(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    verification_data = {
      "SUCCESS_RATE": self.json_data["SUCCESS_RATE"],
      "MAX_POLL_DELAY": self.json_data["MAX_POLL_DELAY"],
      "MAX_WEBHOOK_DELAY": self.json_data["MAX_WEBHOOK_DELAY"]
    }
    host = os.environ['NATIVE_PATH'] if 'NATIVE_PATH' in os.environ else 'http://localhost:3010'
    token = os.environ['SECRET_TOKEN'] if 'SECRET_TOKEN' in os.environ else 'qwerty'
    try:
      response = requests.post(
          f'{host}/native/env',
          json=verification_data
      )
    except: 
       raise NotFoundException
    
    if response.status_code == 200:
        new_user = {
        "RUV": 0
        }
        return new_user
    else: 
        raise NotFoundException