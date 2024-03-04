from flask import jsonify
from ..adapters.service_adapter import ServiceAdapter
from ..errors.errors import ApiError, BadRequestException, NotFoundException, PermissionDeniedException
from .base_command import BaseCommand
import os
from decimal import Decimal

class Posts(BaseCommand):
  def __init__(self, user_id, token, post_id):
    print(user_id)
    print(token)

    self.user_id = user_id
    self.token = token
    self.post_id = post_id
  
  def execute(self):
    # 1. get post
    post = self.getPost()
    print(post)
    # 2. validate user
    if str(post["userId"]) != str(self.user_id):
      raise PermissionDeniedException()

    # 3. get the route 
    route = self.getRoute(post["routeId"])
    print(route)
    
    # 4. get offers 
    offer_list = self.getOffers()
    print(offer_list)
    offers = []
    offerIds = []
    for offer in offer_list:
      offerIds.append(str(offer["id"]))
    
    # 5. get scores
    scores = self.getScores(offerIds)
    print(scores)
    for offer in offer_list:
      score = 0
      for item in scores:
          if str(offer["id"]) == item["offerid"]:
              score = item['profit']
              break
          
      offers.append({
            "id": offer["id"],
            "userId": offer["userId"],
            "description": offer["description"],
            "size": offer["size"],
            "fragile": offer["fragile"],
            "offer": offer["offer"],
            "score": score,
            "createdAt": offer["createdAt"]
          })
      
    # 6. sort offers by score
    offers.sort(key=lambda x: Decimal(x["score"]), reverse = True)
      
    # 7. build the response body  
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
    
    host = os.environ['POSTS_PATH'] if 'POSTS_PATH' in os.environ else 'http://api_post:3001'

    response = ServiceAdapter().resquest(
        'get',
        f'{host}/posts/{self.post_id}',
        {
          'Authorization': f'{self.token}'
        },
        {}
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
    
    host = os.environ['ROUTES_PATH'] if 'ROUTES_PATH' in os.environ else 'http://api_route:3002'

    response = ServiceAdapter().resquest(
      'get',
      f'{host}/routes/{route_id}',
      {
        'Authorization': f'{self.token}'
      },
      {}
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
     
    host = os.environ['OFFERS_PATH'] if 'OFFERS_PATH' in os.environ else 'http://api_offer:3003'
    
    response = ServiceAdapter().resquest(
      'get',
      f'{host}/offers?post={self.post_id}',
      {
        'Authorization': f'{self.token}'
      },
      {}
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
    host = os.environ['SCORES_PATH'] if 'SCORES_PATH' in os.environ else 'http://api_score:3004'

    response = ServiceAdapter().resquest(
      'get',
      f'{host}/scores',
      {
        'Authorization': f'{self.token}'
      },
      {}
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