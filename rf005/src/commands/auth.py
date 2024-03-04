from ..adapters.service_adapter import ServiceAdapter
from ..errors.errors import *
from .base_command import BaseCommand
import os

class Auth(BaseCommand):
    def __init__(self, token):
        self.token = token

    def execute(self):
        if not self.token:
            raise PermissionDeniedException()

        host = os.environ['INGRESS_PATH'] if 'INGRESS_PATH' in os.environ else 'http://api_user:3000'
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
            raise AuthenticationException()
        elif response.status_code == 404:
            raise NotFoundException()
        else:
            raise ApiError(response.status_code)
        