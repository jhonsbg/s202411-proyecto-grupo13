from .base_command import BaseCommand
from ..models.offer import Offer
from ..errors.errors import *
from datetime import datetime, timezone
import os
import requests

class Create(BaseCommand):
    def __init__(self, json_data, token, user_id, id):
        self.post_id = id
        self.user_id = user_id
        self.token = token
        self.json_data = json_data

    def execute(self):
        host = os.environ['OFFERS_PATH'] if 'OFFER_PATH' in os.environ else 'http://localhost:3003'
        # host_post = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://localhost:3001'
        
        try:

            offer = Offer(
                postid = self.post_id,
                userid = self.user_id,
                description = self.json_data['description'],
                size = self.json_data['size'],
                fragile = self.json_data['fragile'],
                offer = self.json_data['offer']
            )

        except KeyError as e:
            print("31")
            raise IncompleteParams(f"Campo faltante en la solicitud: {e}")

        #Validar si existe el post
        post_exists = self.validate_post(self.post_id)

        if (post_exists is not None):

            #validar que el post no es del mismo usuario
            if post_exists['userId'] == self.user_id:
               raise IsUserPost()

            if datetime.strptime(str(post_exists['expireAt']), '%Y-%m-%dT%H:%M:%S.%f') < datetime.now():
                raise InvalidDateExpire()

            #obtener el route
            route = self.get_route(post_exists['routeId'])
            print(route)
            
            #crear la oferta
            reponse = requests.post(
                f'{host}/offers',
                headers={
                    'Authorization': f'{self.token}'
                },
                json={
                    'postId': post_exists['id'],
                    'description': offer.description,
                    'size': offer.size,
                    'fragile': offer.fragile,
                    'offer': offer.offer
                }
            )
            
            if reponse.status_code == 201:
                new_offer = reponse.json()

                #calcular el score
                host_score = os.environ['SCORES_PATH'] if 'SCORES_PATH' in os.environ else 'http://localhost:3004'

                reponse = requests.post(
                    f'{host_score}/scores',
                    headers={
                        'Authorization': f'{self.token}'
                    },
                    json={
                        "userid": self.user_id,
                        "offerid": new_offer['id'],
                        "offer": offer.offer,
                        "size": offer.size,
                        "bagCost": route['bagCost']
                    }
                )
                if reponse.status_code == 201:
                    return {
                        "data": {
                            "postId": post_exists['id'],
                            "userId": self.user_id,
                            "id": new_offer['id'],
                            "createdAt": new_offer['createdAt'],
                            "offer": offer.offer
                        },
                        "msg": 'resumen de la operacion *.'
                    }
                else:
                    raise ApiError()
            else:
                raise ApiError()
        
        else:
            raise PostNotFoundError()
    
    def validate_post(self, id):
        host_post = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://localhost:3001'
        response = requests.get(
            f'{host_post}/posts/{id}',
            headers={
            'Authorization': f'{self.token}'
            }
        )
        if response.status_code == 200:
            post = response.json()
            return post
        else:
            return None

    def get_route(self, id):
        host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'http://localhost:3002'
        print(f'{host}/routes/{id}')
        response = requests.get(
            f'{host}/routes/{id}',
            headers={
            'Authorization': f'{self.token}'
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None