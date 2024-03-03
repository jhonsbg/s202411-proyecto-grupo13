from .service_mock import ServiceMock
from ..errors.errors import *
import requests
import os

class ServiceAdapter():

    def resquest(self, method, path, headers, data):
        if os.environ.get('TESTING') is not None and bool(os.environ.get('TESTING')): 
           print('hola')
           return ServiceMock().resquest(method, path, headers, data)
        else:
            print('hola2')
            return requests.request(
                method,
                path,
                headers=headers,
                json=data
            )