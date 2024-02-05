from ..errors.errors import PreconditionFailedException, BadRequestException
from .base_command import BaseCommannd
from ..models import db, User, StatusEnum

class Create(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    try:
      user = User( \
          username = self.json_data["username"], \
          password = self.json_data["password"], \
          email = self.json_data["email"], \
          dni = self.json_data["dni"], \
          fullName = self.json_data["fullName"], \
          phoneNumber = self.json_data["phoneNumber"], \
          status = StatusEnum.POR_VERIFICAR
      )
    except: 
       raise BadRequestException()
       
    if User.query.filter_by(username=user.username).count() > 0:
        raise PreconditionFailedException()
    
    if User.query.filter_by(email=user.email).count() > 0:
        raise PreconditionFailedException()
    
    db.session.add(user)
    db.session.commit()
    
    created_at = user.createat

    if isinstance(created_at, tuple):
        created_at = created_at[0]

    new_user = {
        "id": user.id,
        "createdAt": created_at.isoformat()
    }
    return new_user
