from ..adapters.service_adapter import ServiceAdapter
from ..errors.errors import *
from .base_command import BaseCommand
import requests
import os

class Autorizacion(BaseCommand):
    def __init__(self, token):
        self.token = token

    def execute(self):
        print(self.token)
        if not self.token:
            raise NoTokenRequest()
 
        host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'http://localhost:3000'
        response = ServiceAdapter().resquest(
            'get',
            f'{host}/users/me',
            {
            'Authorization': f'{self.token}'
            },
            {}
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Unauthorized()
        else: 
            raise ExternalError(response.status_code)