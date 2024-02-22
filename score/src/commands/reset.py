from ..models import db, Score
from .base_command import BaseCommannd

class Reset(BaseCommannd):
 
  def execute(self):
    scores = Score.query.all()

    for score in scores:
        db.session.delete(score)

    db.session.commit()

    return True