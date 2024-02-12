from ..errors.errors import *
from .base_command import BaseCommannd
import requests
import os


class Autorizacion(BaseCommannd):
    def __init__(self, token):
        self.token = token

    def execute(self):
        if not self.token:
            raise AuthenticationException()

        host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'http://localhost:3000'
        endpoint = '/users/me'

        # Configurar la cabecera con el token
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(f'{host}/users/me', headers=headers)
        if response.status_code == 200:
            print(response.status_code)
            return response.status_code
        elif response.status_code == 401:
            raise Unauthorized()
        else: 
            raise ExternalError(response.status_code)