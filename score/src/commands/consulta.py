from ..models import db, Score, ScoreSchema
from ..errors.errors import *
from .base_command import BaseCommannd
import uuid

score_schema = ScoreSchema()

class Consulta(BaseCommannd):
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        required_fields = ["userid", "offerid"]
        
        for field in required_fields:
            if not self.json_data.get(field):
                raise BadRequestException
        try:
            existing_score = Score.query.filter_by(userid=self.json_data["userid"], offerid= self.json_data["offerid"]).all()
            serialized_scores = [score_schema.dump(score) for score in existing_score]
            return serialized_scores 
        except: 
            raise NotFoundException()