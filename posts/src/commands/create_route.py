from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ExternalError
import requests
from flask import jsonify
import os

class CreateRoute(BaseCommannd):
  def __init__(self, token, data):
    self.token = token
    self.data = data

  def execute(self):
    host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'localhost'
    port = os.environ['ROUTES_PORT'] if 'ROUTES_PORT' in os.environ else 3003
    base_path = f'http://{host}:{port}'
    response = requests.post(
      f'{base_path}/routes',
      headers={
        'Authorization': f'{self.token}'
      },
      json=self.data
    )
    print(response.status_code)
    if response.status_code == 201:
      return response.json()
    if response.status_code == 412:
      return None
    else:
      raise ExternalError(response.status_code)