import pytz
from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetPosts(BaseCommannd):
  def __init__(self, data, userId = None):
    try:
      self.expire = data['expire'] if 'expire' in data else None
      self.routeId = data['route'] if 'route' in data else None
      self.owner = data['owner'] if 'owner' in data else None
      self.userId = userId
      self.dateNow = datetime.fromisoformat(str(datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'))
    except ValueError:
      raise InvalidParams()

  def execute(self):

    if self.expire not in ('true', 'false', None):
      raise InvalidParams

    session = Session()
    posts = session.query(Post).all()

    if self.owner == 'me':
      posts = [post for post in posts if str(post.userId) == str(self.userId)]
    
    if self.owner != None and self.owner != 'me':
      posts = [post for post in posts if str(post.userId) == str(self.owner)]

    if self.routeId != None:
      posts = [post for post in posts if str(post.routeId) == str(self.routeId)]

    if self.expire == 'true':
      posts = [post for post in posts if datetime.fromisoformat(str(post.expireAt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00')) < self.dateNow]
    
    if self.expire == 'false':
      posts = [post for post in posts if datetime.fromisoformat(str(post.expireAt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00')) > self.dateNow]

    posts = PostSchema(many=True).dump(posts)
    session.close()

    return posts