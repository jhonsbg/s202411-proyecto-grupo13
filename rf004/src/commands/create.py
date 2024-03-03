import uuid
from .base_command import BaseCommand
from ..models.post import Post
from ..models.offer import Offer
from ..errors.errors import IncompleteParams, InvalidDates, RouteExists, InvalidDateExpire
from flask import request
from datetime import datetime, timezone
import os
import requests
import json

class Create(BaseCommand):
    def __init__(self, json_data, token, user_id, id):
        self.post_id = id
        self.user_id = user_id
        self.token = token
        self.json_data = json_data

    def execute(self):
        host = os.environ['OFFER_PATH'] if 'OFFER_PATH' in os.environ else 'http://localhost:3003'
        host_post = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://localhost:3001'
        
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
            raise IncompleteParams(f"Campo faltante en la solicitud: {e}")

        #Validar si existe el post
        post_exists = self.validate_post(self.post_id)

        if (post_exists):
            #crear la oferta
            reponse = requests.post(
                f'{host}/offers',
                headers={
                    'Authorization': f'{self.token}'
                },
                json={
                    'postid': post_exists['id'],
                    'userid': offer.userid,
                    'description': offer.description,
                    'size': offer.size,
                    'fragile': offer.fragile,
                    'offer': offer.offer
                }
            )
            new_offer = reponse.json()

            return new_offer
        
        else:
            raise InvalidDates()
    
    def validate_post(self, id):
        host_post = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://localhost:3001'
        response = requests.get(
            f'{host_post}/posts/{id}',
            headers={
            'Authorization': f'{self.token}'
            }
        )
        post = response.json()
        if response.status_code == 200:
            return post
        else:
            return None

    