from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ExternalError, NoTokenRequest, Unauthorized
import requests
from flask import jsonify
import os

class Authenticate(BaseCommannd):
  def __init__(self, token):
    self.token = token

  def execute(self):

    if not self.token:
      raise NoTokenRequest()

    host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'localhost'
    response = requests.get(
      f'{host}/users/me',
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return response.json()
    elif response.status_code == 401:
      raise Unauthorized()
    else:
      raise ExternalError(response.status_code)
