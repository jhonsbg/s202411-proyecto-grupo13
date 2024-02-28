import os

import requests
from flask import jsonify

from ..errors.errors import ExternalError
from ..session import Session
from .base_command import BaseCommannd


class GetRoutes(BaseCommannd):
  def __init__(self, token):
    self.token = token

  def execute(self):
    host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'localhost'
    port = os.environ['ROUTES_PORT'] if 'ROUTES_PORT' in os.environ else 3003
    base_path = f'http://{host}:{port}'
    response = requests.get(
      f'{base_path}/routes',
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return response.json()
    else:
      raise ExternalError(response.status_code)