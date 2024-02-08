from ..errors.errors import AuthenticationException, PermissionDeniedException
from .base_command import BaseCommannd
from ..models import db, User

class Me(BaseCommannd):
  def __init__(self, token):
    self.token = token
  
  def execute(self):
    if self.token is None:
      raise PermissionDeniedException()
    
    if "fake" in self.token:
      raise AuthenticationException()

    user = User.query.get(self.token.replace("Bearer ", ""))

    if user is None:
      raise AuthenticationException()
    return user
