from ..errors.errors import ApiError, BadRequestException, NotFoundException, PermissionDeniedException
from .base_command import BaseCommand
import requests

class Posts(BaseCommand):
  def __init__(self, user_id, token, post_id):
    self.user_id = user_id
    self.token = token
    self.post_id = post_id
    #self.host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'http://api_posts:3000'
    self.host = None
  
  def execute(self):
    # 1. get post
    post = self.getPost()

    # 2. validate user
    if str(post["userId"]) != str(self.user_id):
      raise PermissionDeniedException()

    # 3. get the route 
    route = self.getRoute(post["routeId"])
    
    # 4. get offers 
    offer_list = self.getOffers()
    offers = []
    offerIds = []
    for offer in offer_list:
      offerIds.append(str(offer["id"]))
      offers.append({
            "id": offer["id"],
            "userId": offer["userId"],
            "description": offer["description"],
            "size": offer["size"],
            "fragile": offer["fragile"],
            "offer": offer["offer"],
            "score": 0,
            "createdAt": offer["createdAt"]
          })
    
    # 5. get scores
    # scores = self.getScores(offerIds)
    # 6. sort offers by score
    # for offer in offer_list:
    #   offerIds.append(str(offer["id"]))
    #   offers.append({
    #         "id": offer["id"],
    #         "userId": offer["userId"],
    #         "description": offer["description"],
    #         "size": offer["size"],
    #         "fragile": offer["fragile"],
    #         "offer": offer["offer"],
    #         "score": 0,
    #         "createdAt": offer["createdAt"]
    #       })

    response = {
      "data": {
        "id": post["id"],
        "expireAt": post["expireAt"],
        "route": {
          "id": route["id"],
          "flightId": route["flightId"],
          "origin": {
            "airportCode": route["sourceAirportCode"],
            "country": route["sourceCountry"]
          },
          "destiny": {
              "airportCode": route["destinyAirportCode"],
              "country": route["destinyCountry"]
          },
          "bagCost": route["bagCost"]
        },
        "plannedStartDate": route["plannedStartDate"],
        "plannedEndDate": route["plannedEndDate"],
        "createdAt": post["createdAt"],
        "offers": offers
      }
    }
    return response

  def getPost(self):
    if self.post_id is None:
      raise BadRequestException()
    
    host = self.host or 'http://localhost:3001'
    response = requests.get(
        f'{host}/posts/{self.post_id}',
        headers={
        'Authorization': f'{self.token}'
        }
    )

    if response.status_code == 200:
      try:
        return response.json()
      except: 
        raise NotFoundException()
    elif response.status_code == 404:
        raise NotFoundException()
    else:
      raise ApiError(response.status_code)

  def getRoute(self, route_id):
    if route_id is None:
      raise NotFoundException()
    
    host = self.host or 'http://localhost:3002'
    response = requests.get(
        f'{host}/routes/{route_id}',
        headers={
        'Authorization': f'{self.token}'
        }
    )

    if response.status_code == 200:
      try:
        return response.json()
      except: 
        raise NotFoundException()
    elif response.status_code == 404:
        raise NotFoundException()
    else:
      raise ApiError(response.status_code)
    
  def getOffers(self):
    if self.post_id is None:
      raise BadRequestException()
     
    host = self.host or 'http://localhost:3003'
    response = requests.get(
        f'{host}/offers?post={self.post_id}',
        headers={
        'Authorization': f'{self.token}'
        }
    )

    if response.status_code == 200:
      try:
        return response.json()
      except: 
        raise NotFoundException()
    elif response.status_code == 404:
        raise NotFoundException()
    else:
      raise ApiError(response.status_code)
    
  def getScores(self, offerIds):
    
    host = self.host or 'http://localhost:3003'
    response = requests.post(
        f'{host}/scores',
        headers={
        'Authorization': f'{self.token}'
        },
        data=offerIds
    )

    if response.status_code == 200:
      try:
        return response.json()
      except: 
        raise NotFoundException()
    elif response.status_code == 404:
        raise NotFoundException()
    else:
      raise ApiError(response.status_code)