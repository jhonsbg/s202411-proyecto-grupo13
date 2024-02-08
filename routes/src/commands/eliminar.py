from models import db, Route
from errors.errors import *
from .base_command import BaseCommannd
from datetime import datetime
import uuid

class Eliminar(BaseCommannd):
  def __init__(self, id, token):
    self.id = id
    self.token = token

  @staticmethod
  def is_valid_token(token):
    #return token in valid_tokens
    return token=="Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"
  
  def execute(self): 
    try:
      if not self.token:
        raise PermissionDeniedException()   
      
      try:
          uuid.UUID(self.id)
      except ValueError:
          raise BadRequestException()
      if self.is_valid_token(self.token):        
        existing_id = Route.query.get(self.id)
        if existing_id:
            db.session.delete(existing_id)
            db.session.commit()
            return True
        else:
          raise SolicitudException()
      else:
        raise AuthenticationException()
    except:
        raise SolicitudException()
    