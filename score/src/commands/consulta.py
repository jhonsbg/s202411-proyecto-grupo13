from ..models import db, Score, ScoreSchema
from ..errors.errors import *
from .base_command import BaseCommannd

score_schema = ScoreSchema()

class Consulta(BaseCommannd):
    # def __init__(self, json_data):
        # self.json_data = json_data

    def execute(self):
        # offerIds = []
        
        # for id in self.json_data["data"]:
        #     offerIds.append(str(id))

        # try:
            # existing_scores = Score.query.filter(Score.offerid.in_(offerIds)).all()
            existing_scores = Score.query.all()
            serialized_scores = [score_schema.dump(score) for score in existing_scores]
            return serialized_scores 
        # except: 
        #     raise NotFoundException()