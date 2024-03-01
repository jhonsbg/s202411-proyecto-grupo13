from ..errors.errors import *
from .base_command import BaseCommand
import requests
import os

class Auth(BaseCommand):
    def __init__(self, token):
        self.token = token

    def execute(self):
        if not self.token:
            raise PermissionDeniedException()
        
        if os.environ.get('TESTING') is not None and bool(os.environ.get('TESTING')): 
            if self.token is None:
                raise AuthenticationException()
                
            if "fake" in self.token:
                raise BadRequestException()

            if self.token != "Bearer cd3d1303-2d62-4f60-8472-3349d34f690c":
                raise AuthenticationException()
            return 'ok'

        host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'http://localhost:3000'
        response = requests.get(
            f'{host}/users/me',
            headers={
            'Authorization': f'{self.token}'
            }
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthenticationException()
        elif response.status_code == 404:
            raise NotFoundException()
        else:
            raise ApiError(response.status_code)