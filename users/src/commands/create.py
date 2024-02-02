from ..errors.errors import PreconditionFailedException
from .base_command import BaseCommannd
from ..models import db, User

class Create(BaseCommannd):
  def __init__(self, user):
    self.user = user
  
  def execute(self):
    if User.query.filter_by(username=self.user.username).count() > 0:
        raise PreconditionFailedException()
    
    if User.query.filter_by(email=self.user.email).count() > 0:
        raise PreconditionFailedException()
    
    db.session.add(self.user)
    db.session.commit()
    
    created_at = self.user.createat

    if isinstance(created_at, tuple):
        created_at = created_at[0]

    new_user = {
        "id": self.user.id,
        "createdAt": created_at.isoformat()
    }
    return new_user
