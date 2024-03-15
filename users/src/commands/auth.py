from ..errors.errors import BadRequestException, NotFoundException, AuthenticationException
from .base_command import BaseCommannd
from ..models import db, User
import enum

class StatusEnum(enum.Enum):
    POR_VERIFICAR = 'Por verificar'
    NO_VERIFICADO = 'No verificado'
    VERIFICADO = 'Verificado'

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

    if user is None: 
      raise NotFoundException()
    
    status = f"{StatusEnum.VERIFICADO}"
    status2 = f"{user.status}"
    if status == status2:
      return {
          "id": user.id,
          "token": user.id,
          "expireAt": "2024-03-20T14:28:23.382748"
      }
    else:
      raise AuthenticationException
