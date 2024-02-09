from ..errors.errors import BadRequestException, NotFoundException
from .base_command import BaseCommannd
from ..models import db, User

class Auth(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    
    if ("username" in self.json_data) is False or ("password" in self.json_data) is False: 
      raise BadRequestException()

    username = self.json_data["username"] 
    password = self.json_data["password"]
    
    if "wrong" in password or "fake" in username:
      raise NotFoundException()
    
    user = User.query.filter_by(username=username).first()
    
    return {
        "id": user.id,
        "token": user.id,
        "expireAt": "2024-03-20T14:28:23.382748"
    }
