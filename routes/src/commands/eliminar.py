from ..models import db, Route
from ..errors.errors import *
from .base_command import BaseCommannd
from datetime import datetime
from flask import make_response, jsonify
import uuid

class Eliminar(BaseCommannd):
  def __init__(self, id):
    self.id = id

  def execute(self):
    try:
        uuid.UUID(self.id)
    except ValueError:
        raise BadRequestException() 
    try:    
      existing_id = Route.query.get(self.id)
      if existing_id:
          db.session.delete(existing_id)
          db.session.commit()
          serialized_new_route = {
            "msg": "el trayecto fue eliminado"
          }
          return make_response(jsonify(serialized_new_route), 200)
      else:
        raise NotFoundException()
    except:
        raise NotFoundException()
    