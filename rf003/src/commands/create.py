import uuid
from .base_command import BaseCommand
from ..models.post import Post
from ..models.route import Route
from ..errors.errors import IncompleteParams, InvalidDates, RouteExists, Prueba
from flask import request
from datetime import datetime
import os
import requests
import json

class Create(BaseCommand):
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        token = request.headers.get('Authorization')
        host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'http://api_routes:3002'
        host_post = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://api_posts:3001'
        
        try:
            planned_start_date = datetime.strptime(self.json_data['plannedStartDate'], '%Y-%m-%dT%H:%M:%S')
            planned_end_date = datetime.strptime(self.json_data['plannedEndDate'], '%Y-%m-%dT%H:%M:%S')
            expire_at = datetime.strptime(self.json_data['expireAt'], '%Y-%m-%dT%H:%M:%S')

            route = Route(\
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
        
        if planned_start_date > datetime.now() and expire_at > datetime.now() and expire_at <= planned_start_date:
            print("ingreso por fechas correctas")
            route_id = self.validate_route(route.flightId, token)
            if route_id:
                print("ingreso por ruta existente")
                
                response = requests.get(
                    f'{host}/routes',
                    headers={
                    'Authorization': f'{token}'
                    }
                )
                routes_data = response.json()
                old_route = next((route for route in routes_data if route['flightId'] == route.flightId), None)

                post = Post(\
                    routeId = old_route.id , \
                    userId = token.replace("Bearer ", ""), \
                    expireAt = expire_at, \
                )

                old_route_id = self.validate_route_id(post.routeId, token)
                
                if old_route_id:
                    raise RouteExists()
                
                else:
                    
                    response = requests.post(
                        f'{host_post}/posts',
                        json=post.serialize(), 
                        headers={
                            'Authorization': f'{token}'
                        }
                    )
                    new_post = response.json()
                    ##Falta validar la consistencia en caso de alguna falla
            else:
                post = Post(\
                    routeId = route.id , \
                    userId = token.replace("Bearer ", ""), \
                    expireAt = expire_at, \
                )

                old_route_id = self.validate_route_id(post.routeId, token)

                if old_route_id:
                    raise RouteExists()
                
                else:
                    response = requests.post(
                        f'{host_post}/posts',
                        json=post.serialize(), 
                        headers={
                            'Authorization': f'{token}'
                        }
                    )

                    if response.status_code == 200:
                        try:
                            new_post = response.json()
                        except json.JSONDecodeError:
                            print("La respuesta no contiene datos JSON")
                    else:
                        print(f"Solicitud fallida con código de estado: {response.status_code}")

            created_at_post = post.createdAt

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
        
        else:
            raise InvalidDates()
    
    def validate_route(self, flightId,token):
        
        host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'http://api_routes:3002'
        response = requests.get(
            f'{host}/routes',
            headers={
            'Authorization': f'{token}'
            }
        )
        if response.status_code == 200 and response.json() != []:
            routes_data = response.json()

            existing_route = next((route for route in routes_data if route['flightId'] == flightId), None)

            if existing_route:
                return True
            else:
                return False
        else:
            return False

    def validate_route_id(self, routeId, token):

        host = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://api_posts:3001'
        response = requests.get(
            f'{host}/posts',
            headers={
            'Authorization': f'{token}'
            }
        )

        if response.status_code == 200:
            posts_data = response.json()

            existing_post_with_route_id = next((post for post in posts_data if post['routeId'] == routeId), None)

            if existing_post_with_route_id:
                return True
            else:
                return False
        else:
            return False