from models import db, Route
from .base_command import BaseCommannd

class Reset(BaseCommannd):
 
  def execute(self):
    routes = Route.query.all()

    for route in routes:
        db.session.delete(route)

    db.session.commit()

    return True