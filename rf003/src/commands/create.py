from ..adapters.service_adapter import ServiceAdapter
from .base_command import BaseCommand
from ..models.post import Post
from ..models.route import Route
from ..errors.errors import IncompleteParams, InvalidDates, RouteExists, InvalidDateExpire
from datetime import datetime, timezone
import os

class Create(BaseCommand):
    def __init__(self, json_data, token, user_id):
        self.user_id = user_id
        self.token = token
        self.json_data = json_data

    def execute(self):
        host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'http://localhost:3002'
        host_post = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://localhost:3001'
        
        try:
            planned_start_date = datetime.strptime(str(self.json_data['plannedStartDate']), '%Y-%m-%dT%H:%M:%S.%f%z')
            planned_end_date = datetime.strptime(str(self.json_data['plannedEndDate']), '%Y-%m-%dT%H:%M:%S.%f%z')
            expire_at = datetime.strptime(str(self.json_data['expireAt']), '%Y-%m-%dT%H:%M:%S.%f%z')

            route = Route(
                flightId=self.json_data['flightId'],
                plannedStartDate = self.json_data['plannedStartDate'],
                plannedEndDate = self.json_data['plannedEndDate'],
                sourceAirportCode=self.json_data['origin']['airportCode'],
                sourceCountry=self.json_data['origin']['country'],
                destinyAirportCode=self.json_data['destiny']['airportCode'],
                destinyCountry=self.json_data['destiny']['country'],
                bagCost=self.json_data['bagCost'],
            )

            # Convierte a datetime solo si plannedStartDate es una cadena
            if isinstance(route.plannedStartDate, str):
                route.plannedStartDate = datetime.strptime(route.plannedStartDate, '%Y-%m-%dT%H:%M:%S.%f%z')
            # Convierte a datetime solo si plannedEndDate es una cadena
            if isinstance(route.plannedEndDate, str):
                route.plannedEndDate = datetime.strptime(route.plannedEndDate, '%Y-%m-%dT%H:%M:%S.%f%z')

            # Ahora puedes aplicar isoformat y agregar 'Z'
            route.plannedStartDate = route.plannedStartDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            route.plannedEndDate = route.plannedEndDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        except KeyError as e:
            raise IncompleteParams(f"Campo faltante en la solicitud: {e}")
        
        if expire_at < datetime.now(timezone.utc):
            raise InvalidDateExpire()

        print((
            planned_start_date > datetime.now(timezone.utc)
            and planned_end_date > datetime.now(timezone.utc)
            and expire_at > datetime.now(timezone.utc)
            and expire_at <= planned_start_date
        ))
        if (
            planned_start_date > datetime.now(timezone.utc)
            and planned_end_date > datetime.now(timezone.utc)
            and expire_at > datetime.now(timezone.utc)
            and expire_at <= planned_start_date
        ):
            route_id = self.validate_route(route.flightId)
            if route_id:
                
                response = ServiceAdapter().resquest(
                    'get',
                    f'{host}/routes',
                    {
                        'Authorization': f'{self.token}'
                    },
                    {}
                )
                print("/routes 69")
                print(response.json())

                routes_data = response.json()
                old_route = next((route for route in routes_data if route['flightId'] == route['flightId']), None)

                post = Post(\
                    routeId = old_route['id'] , \
                    userId = self.user_id, \
                    expireAt = expire_at, \
                )

                old_route_id = self.validate_route_id(post.routeId)
                
                if old_route_id:
                    raise RouteExists()
                
                else:
                    response = ServiceAdapter().resquest(
                        'post',
                        f'{host_post}/posts',
                        {
                        'Authorization': f'{self.token}'
                        },
                        post.serialize()
                    )
                    print("/routes 94")
                    print(response.json())
                    new_post = response.json()
                    ##Falta validar la consistencia en caso de alguna falla
            else:
                post = Post(\
                    routeId = route.id , \
                    userId = self.user_id, \
                    expireAt = expire_at, \
                )

                old_route_id = self.validate_route_id(post.routeId)

                if old_route_id:
                    raise RouteExists()
                
                #En caso que no exista el trayecto, se procede a crearlo junto con el post
                else:
                    #persistir trayecto
                    response = ServiceAdapter().resquest(
                        'post',
                        f'{host}/routes',
                        {
                        'Authorization': f'{self.token}'
                        },
                        route.serialize()
                    )

                    if response.status_code == 201:
                        new_route = response.json()
                        route.id = new_route["id"]
                    else:
                        raise RouteExists()

                    #persistir post
                    response = ServiceAdapter().resquest(
                        'post',
                        f'{host_post}/posts',
                        {
                        'Authorization': f'{self.token}'
                        },
                        post.serialize()
                    )
                    print("/posts 138")
                    print(response.json())

                    if response.status_code == 200:
                        new_post = response.json()

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
                            "id": old_route['id'],
                            "createdAt": old_route['createdAt'],
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
    
    def validate_route(self, flightId):
        
        host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'http://localhost:3002'
        response = ServiceAdapter().resquest(
            'get',
            f'{host}/routes',
            {
                'Authorization': f'{self.token}'
            },
            {}
        )
        print("/routes 210")
        print(response.json())

        if response.status_code == 200 and response.json() != []:
            routes_data = response.json()

            existing_route = next((route for route in routes_data if route['flightId'] == flightId), None)

            if existing_route:
                return True
            else:
                return False
        else:
            return False

    def validate_route_id(self, routeId):

        host = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://localhost:3001'
        response = ServiceAdapter().resquest(
            'get',
            f'{host}/posts',
            {
                'Authorization': f'{self.token}'
            },
            {}
        )
        print("/posts 236")
        print(response.json())

        if response.status_code == 200:
            posts_data = response.json()

            existing_post_with_route_id = next((post for post in posts_data if post['routeId'] == routeId), None)

            if existing_post_with_route_id:
                return True
            else:
                return False
        else:
            return False