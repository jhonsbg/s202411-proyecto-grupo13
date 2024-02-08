from ..errors.errors import AuthenticationException
from .base_command import BaseCommannd
from ..models import db, User

class Me(BaseCommannd):
  def __init__(self, token):
    self.token = token
  
  def execute(self):
    if "fake" in self.token:
      raise AuthenticationException()

    return User.query.get_or_404(self.token.replace("Bearer ", ""))
