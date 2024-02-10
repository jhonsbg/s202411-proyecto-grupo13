from ..models import db, Offer
from .base_command import BaseCommand
from flask import make_response, jsonify

class Reset(BaseCommand):
  def execute(self):
    offers = Offer.query.all()
    for offer in offers:
        db.session.delete(offer)
    db.session.commit()
    msg = {
            "msg": "Todos los datos fueron eliminados"
         }
    response = make_response(jsonify(msg), 200)
    return response