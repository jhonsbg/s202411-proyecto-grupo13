from ..models import db, Card
from .base_command import BaseCommand
from flask import make_response, jsonify

class Reset(BaseCommand):
  def execute(self):
    cards = Card.query.all()
    for card in cards:
      db.session.delete(card)
    db.session.commit()
    msg = {
            "msg": "Todos los datos fueron eliminados"
         }
    response = make_response(jsonify(msg), 200)
    return response