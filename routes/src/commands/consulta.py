from models import db, Route, RouteSchema
from errors.errors import *
from .base_command import BaseCommannd
import uuid

route_schema = RouteSchema()

class Consulta(BaseCommannd):
    def __init__(self, id, token):
        self.id = id
        self.token = token

    def execute(self):    
        try:
            if not self.token:
               raise PermissionDeniedException()
            
            try:
                uuid.UUID(self.id)
            except ValueError:
                raise BadRequestException()
            
            existing_id = Route.query.get(self.id)
            if existing_id:    
                serialized_id = route_schema.dump(existing_id)
                return serialized_id
            else:
                raise PermissionDeniedException()
        except: 
            raise SolicitudException()