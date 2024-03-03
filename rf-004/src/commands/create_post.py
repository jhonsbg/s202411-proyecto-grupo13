from marshmallow import ValidationError
from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates
from datetime import datetime, timezone
import pytz
import uuid

class CreatePost(BaseCommannd):
  def __init__(self, data, userId = None):
    self.data = data
    if 'expireAt' in data:
      self.data['expireAt'] = datetime.fromisoformat(str(data['expireAt'].replace('Z', '+00:00')))
    else:
      raise IncompleteParams
    
    if 'routeId' in data:
      self.data['routeId'] = data['routeId']
    else:
      raise IncompleteParams
    
    if userId != None:
      self.data['userId'] = userId
    else:
      raise IncompleteParams
    
    self.data['createdAt'] = datetime.fromisoformat(str(datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'))
  
  def execute(self):
    try:
      if not self.valid_dates():
        raise InvalidDates()

      try:
        post = Post(\
          id = str(uuid.uuid4()), \
          routeId = self.data['routeId'], \
          userId = self.data['userId'], \
          expireAt = self.data['expireAt'], \
          createdAt = self.data['createdAt'], \
        )
      except ValidationError as e:
        raise IncompleteParams(str(e))

      session = Session()

      session.add(post)
      session.commit()

      new_post = PostSchema().dump(post)
      session.close()

      return new_post
    # except TypeError:
    except ValidationError as e:
      raise IncompleteParams(str(e))

  def valid_dates(self):
    created = self.data['createdAt']
    expired = self.data['expireAt']
    validation = created < expired
    return validation