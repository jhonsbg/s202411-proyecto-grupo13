from ..models import db, Route, RouteSchema
from ..errors.errors import *
from .base_command import BaseCommannd
import requests
import os

route_schema = RouteSchema()

class Autorizacion(BaseCommannd):
    def __init__(self, token):
        self.token = token

    def execute(self):
        if not self.token:
            raise AuthenticationException()
        host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'localhost'
        port = os.environ['USERS_PORT'] if 'USERS_PORT' in os.environ else 3000
        base_url = f'http://{host}:{port}'    
        endpoint = '/users/me'
        full_url = base_url + endpoint

        # Configurar la cabecera con el token
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(full_url, headers=headers)
        return response.status_code