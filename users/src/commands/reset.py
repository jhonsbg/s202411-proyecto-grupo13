from ..models import db, User
from .base_command import BaseCommannd

class Reset(BaseCommannd):
  
  def execute(self):
    users = User.query.all()

    for user in users:
        db.session.delete(user)

    db.session.commit()

    return True
