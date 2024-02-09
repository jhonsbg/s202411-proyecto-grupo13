from ..errors.errors import BadRequestException
from .base_command import BaseCommannd
from ..models import db, User

class Edit(BaseCommannd):
  def __init__(self, id_user, json_data):
    self.id_user = id_user
    self.json_data = json_data
  
  def execute(self):
    user = User.query.get_or_404(self.id_user)

    if ("status" in self.json_data) is False or ("dni" in self.json_data) is False or ("fullName" in self.json_data) is False or ("phoneNumber" in self.json_data) is False: 
        raise BadRequestException()

    user.status = self.json_data["status"]
    user.dni = self.json_data["dni"]
    user.fullName = self.json_data["fullName"]
    user.phoneNumber = self.json_data["phoneNumber"]

    db.session.commit()

    return True
