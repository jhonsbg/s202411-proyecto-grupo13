import uuid
from ..models import db, Score
from ..errors.errors import *
from .base_command import BaseCommannd
from datetime import datetime
from flask import make_response, jsonify
import enum

class SizeEnum(enum.Enum):
    LARGE = ('Large', 100)
    MEDIUM = ('Medium', 50)
    SMALL = ('Small', 25)


class Calcula(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    required_fields = ["userid", "offerid", "offer", "size", "bagCost"]
        
    for field in required_fields:
        if not self.json_data.get(field):
            raise BadRequestException
            
    offer = self.json_data["offer"]
    size = self.json_data["size"]
    bagCost = self.json_data["bagCost"]

    size_percentage = (SizeEnum[size.upper()].value[1]) / 100
    
    utilidad = offer - ( size_percentage * bagCost )

    try:
        new_score = Score( \
        id = str(uuid.uuid4()), \
        userid = self.json_data["userid"], \
        offerid = self.json_data["offerid"], \
        profit = utilidad \
        )
        db.session.add(new_score)
        db.session.commit()
        serialized_new_score = {
            "id": new_score.id,
            "profit": new_score.profit
        }
        return make_response(jsonify(serialized_new_score), 201)
    except: 
        raise BadRequestException()
    
      
    
    
  