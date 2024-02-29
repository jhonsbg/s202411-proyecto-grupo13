import uuid
from .base_command import BaseCommand
from ..models.post import Post, db
from ..models.route import Route, db
from ..errors.errors import IncompleteParams
from flask import request
from datetime import datetime

class Create(BaseCommand):
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        token = request.headers.get('Authorization')
        
        try:
            planned_start_date = datetime.strptime(self.json_data['plannedStartDate'], '%Y-%m-%dT%H:%M:%S')
            planned_end_date = datetime.strptime(self.json_data['plannedEndDate'], '%Y-%m-%dT%H:%M:%S')

            route = Route(\
                id = str(uuid.uuid4()), \
                flightId = self.json_data['flightId'], \
                plannedStartDate = planned_start_date, \
                plannedEndDate = planned_end_date, \
                sourceAirportCode = self.json_data['origin']['airportCode'], \
                sourceCountry = self.json_data['origin']['country'], \
                destinyAirportCode = self.json_data['destiny']['airportCode'], \
                destinyCountry = self.json_data['destiny']['country'], \
                bagCost = self.json_data['bagCost'], \
            )

        except KeyError as e:
            raise IncompleteParams(f"Campo faltante en la solicitud: {e}")

        route_id = self.validate_route(route.flightId)
        expire_at = datetime.strptime(self.json_data['expireAt'], '%Y-%m-%dT%H:%M:%S')

        if route_id:
            old_route = Route.query.filter_by(flightId=route.flightId).first()
            post = Post(\
                id = str(uuid.uuid4()), \
                routeId = old_route.id , \
                userId = token.replace("Bearer ", ""), \
                expireAt = expire_at, \
            )
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(\
                id = str(uuid.uuid4()), \
                routeId = route.id , \
                userId = token.replace("Bearer ", ""), \
                expireAt = expire_at, \
            )
            db.session.add(route)
            db.session.add(post)
            db.session.commit()

        created_at_post = post.createat

        if isinstance(created_at_post, tuple):
            created_at_post = created_at_post[0]

        expire_at_post = post.expireAt

        if isinstance(expire_at_post, tuple):
            expire_at_post = expire_at_post[0]

        created_at_route = route.createdAt if route else None

        if created_at_route is not None and not isinstance(created_at_route, datetime):
            try:
                created_at_route = datetime.fromisoformat(created_at_route)
            except ValueError:
                created_at_route = None

        if created_at_route is not None:
            created_at_route = created_at_route.isoformat()

        if route_id:
            new_post = {
                "data": {
                    "id": post.id,
                    "userId": post.userId,
                    "createdAt": created_at_post.isoformat(),
                    "expireAt": expire_at_post.isoformat(),
                    "route": {
                        "id": old_route.id,
                        "createdAt": old_route.createdAt.isoformat(),
                    }
                },
                "msg": "Resumen de la operación *."
            }
        else:
            new_post = {
                "data": {
                    "id": post.id,
                    "userId": post.userId,
                    "createdAt": created_at_post.isoformat(),
                    "expireAt": expire_at_post.isoformat(),
                    "route": {
                        "id": route.id,
                        "createdAt": created_at_route,
                    }
                },
                "msg": "Resumen de la operación *."
            }

        return new_post
    
    def validate_route(self, flightId):
        existing_route = Route.query.filter_by(flightId=flightId).first()
        if existing_route:
            return True

        return False
