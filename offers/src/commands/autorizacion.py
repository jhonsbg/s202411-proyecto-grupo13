from ..errors.errors import *
from .base_command import BaseCommand
import requests
import os

class Autorizacion(BaseCommannd):
    def __init__(self, token):
        self.token = token

    def execute(self):
        if not self.token:
            raise AuthenticationException()

        host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'localhost'
        endpoint = '/users/me'

        # Configurar la cabecera con el token
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(f'{host}/users/me', headers=headers)
        return response.status_code