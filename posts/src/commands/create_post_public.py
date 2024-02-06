import json
from datetime import datetime, timedelta, timezone

from ..commands.get_posts import GetPosts
from ..errors.errors import IncompleteParams, InvalidDates, PostCreateError
from ..models.post import Post, PostSchema
from ..session import Session
from .base_command import BaseCommannd
from .create_route import CreateRoute
from .get_routes import GetRoutes


class CreatePostPublic(BaseCommannd):
  def __init__(self, data, userId = None, token = None):
    self.data = data
    self.token = token
  
    if 'plannedStartDate' in data:
      self.data['plannedStartDate'] = str(datetime.strptime(data['plannedStartDate'], "%Y-%m-%d"))
    if 'plannedEndDate' in data:
      self.data['plannedEndDate'] = str(datetime.strptime(data['plannedEndDate'], "%Y-%m-%d"))
    if userId != None:
      self.data['userId'] = userId
  
  def execute(self):
    try:
      print("data: ",self.data)
      if not self.valid_dates():
        raise InvalidDates()
      
      if not self.valid_date_planned():
        raise InvalidDates()
      
      if not self.valid_fields():
        raise IncompleteParams()
      dataRouter = self.mapperData()
      dataRoute=CreateRoute(self.token, dataRouter).execute()
      dataPost={}
      getIdRoute = 0
      if dataRoute is None:
        allRoutes= GetRoutes(self.token).execute()
        getIdRoute = self.filterRoute(allRoutes)
        dataPost = self.mapperPostsRouteExits(getIdRoute)
      else:
        dataPost = self.mapperPosts(dataRoute)
      data={}
      data['route'] =getIdRoute
      data['filter'] = 'me'
      allPosts = GetPosts(data, self.data['userId']).execute()
      
      if self.exitsPosts(allPosts, getIdRoute):
        raise PostCreateError
      posted_post = PostSchema(
        only=('routeId', 'userId', 'plannedStartDate', 'plannedEndDate')
      ).load(dataPost)
      post = Post(**posted_post)
      session = Session()

      session.add(post)
      session.commit()

      new_post = PostSchema().dump(post)
      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams

  def valid_dates(self):
    init = datetime.strptime(self.data['plannedStartDate'], "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(self.data['plannedEndDate'], "%Y-%m-%d %H:%M:%S")
    return init < end
  
  def valid_date_planned(self):
    now_date = datetime.now()
    planned_start_date = datetime.strptime(self.data['plannedStartDate'], "%Y-%m-%d %H:%M:%S")
    return planned_start_date >= now_date and planned_start_date < now_date +  timedelta(days=30)
  
  def valid_fields(self):
    if self.data['plannedStartDate'] is None:
      return False
    elif self.data['plannedEndDate'] is None:
      return False
    elif self.data['origin'] is None:
      return False
    elif self.data['destiny'] is None:
      return False  
    elif self.data['bagCost'] is None:
      return False
    else:
      return True 
    
  def mapperData(self):
    dataRoute = {}
    dataRoute['sourceAirportCode'] = self.data['origin']['airportCode']
    dataRoute['sourceCountry'] = self.data['origin']['country']
    dataRoute['destinyAirportCode'] = self.data['destiny']['airportCode']
    dataRoute['destinyCountry'] = self.data['destiny']['country']
    dataRoute['bagCost'] = int(self.data['bagCost'])
    return json.loads(json.dumps(dataRoute))
  
  def mapperPosts(self, dataRoutes):
    dataPost = {}
    dataPost['routeId']=dataRoutes['id']
    dataPost['userId']= self.data['userId']
    dataPost['plannedStartDate']= self.data['plannedStartDate']
    dataPost['plannedEndDate']= self.data['plannedEndDate']
    return json.loads(json.dumps(dataPost))
  
  def mapperPostsRouteExits(self, routeId):
    dataPost = {}
    dataPost['routeId']= routeId
    dataPost['userId']= self.data['userId']
    dataPost['plannedStartDate']= self.data['plannedStartDate']
    dataPost['plannedEndDate']= self.data['plannedEndDate']
    return json.loads(json.dumps(dataPost))
  
  def filterRoute(self, allRoutes):
    for route in allRoutes:
      if (route['sourceAirportCode'] == self.data['origin']['airportCode'] and
        route['sourceCountry'] == self.data['origin']['country'] and
        route['destinyAirportCode'] == self.data['destiny']['airportCode'] and
        route['destinyCountry'] == self.data['destiny']['country']
      ):
        return route['id']

  def exitsPosts(self, allPosts, routeId):
    for post in allPosts:
      if (post['plannedStartDate'].split('T')[0] == self.data['plannedStartDate'].split()[0] and 
          int(post['routeId']) ==  int(routeId)):
        return True
    return False
  