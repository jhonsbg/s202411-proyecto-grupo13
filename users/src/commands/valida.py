from ..errors.errors import BadRequestException
from .base_command import BaseCommannd
from ..models import db, User
import hashlib
import os
from datetime import datetime, timezone, timedelta

class Valida(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    existing_user = User.query.filter_by(dni=self.json_data["userIdentifier"]).first()
    #genera fecha de modificación
    fecha= datetime.now(timezone.utc)
    zona = timezone(timedelta(hours=-5))
    fechazona = fecha.astimezone(zona)
    formato = "%Y-%m-%d %H:%M:%S.%f %z"
    fupdate = fechazona.strftime(formato)
    token = os.environ['SECRET_TOKEN'] if 'SECRET_TOKEN' in os.environ else 'qwerty'
    ruv = self.json_data["RUV"]
    score = self.json_data["score"]
    #validación token
    validaToken = f"{token}:{ruv}:{score}"
    sha_token = hashlib.sha256(validaToken.encode()).hexdigest()
    if sha_token == self.json_data["verifyToken"]: 
      existing_user.status = self.json_data["status"]
      existing_user.updateAt = fupdate
      db.session.commit()
      return True
    else:
      raise BadRequestException()