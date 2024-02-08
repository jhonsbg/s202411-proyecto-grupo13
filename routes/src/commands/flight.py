from models import db, Route, RouteSchema
from errors.errors import *
from .base_command import BaseCommannd

route_schema = RouteSchema()

class VerFligth(BaseCommannd):
    def __init__(self, flight, token):
        self.flight = flight
        self.token = token

    def execute(self):    
        try:
            if not self.token:
               raise PermissionDeniedException()
            if not self.flight:
                routes = Route.query.all()
                serialized_routes = [route_schema.dump(route) for route in routes]
            else:
                existing_flight = Route.query.filter_by(flightId=self.flight).first()
                if existing_flight:
                    serialized_routes = route_schema.dump(existing_flight)
                else:
                    raise SolicitudException()
            return serialized_routes    
        except: 
            raise SolicitudException()