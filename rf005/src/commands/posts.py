from ..errors.errors import ApiError, BadRequestException, NotFoundException, PermissionDeniedException
from .base_command import BaseCommand
import requests
import os

class Posts(BaseCommand):
  def __init__(self, user_id, token, post_id):
    self.user_id = user_id
    self.token = token
    self.post_id = post_id
  
  def execute(self):
    if self.post_id is None:
      raise BadRequestException()
    
    # host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'http://api_posts:3001'
    host = 'http://localhost:3001'
    response = requests.get(
        f'{host}/posts/{self.post_id}',
        headers={
        'Authorization': f'{self.token}'
        }
    )
    if response.status_code == 200:
      try:
        post = response.json()
      except: 
        raise NotFoundException()

      print(post["userId"])
      print(self.user_id)

      if str(post["userId"]) != str(self.user_id):
        raise PermissionDeniedException()

      # TODO:
      # get the route 
      # get offers 
      # get scores
      # sort offers by score

      response = {
        "data": {
          "id": post["id"],
          "expireAt": post["expireAt"],
          "route": {
            "id": post["routeId"],
            "flightId": "",
            "origin": {
              "airportCode": "",
              "country": ""
            },
            "destiny": {
                "airportCode": "",
                "country": ""
            },
            "bagCost": ""
          },
          "plannedStartDate": "",
          "plannedEndDate": "",
          "createdAt": post["createdAt"],
          "offers": [
            {
              "id": "",
              "userId": "",
              "description": "",
              "size": "",
              "fragile": "",
              "offer": "",
              "score": 2,
              "createdAt": ""
            },
            {
              "id": "",
              "userId": "",
              "description": "",
              "size": "",
              "fragile": "",
              "offer": "",
              "score": 1,
              "createdAt": ""
            }
          ]
        }
      }
      return response
    
    elif response.status_code == 404:
        raise NotFoundException()
    else:
      raise ApiError(response.status_code)
