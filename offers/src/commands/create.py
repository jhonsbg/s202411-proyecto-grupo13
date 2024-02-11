import uuid
from .base_command import BaseCommand
from ..models.offer import Offer, db
from ..errors.errors import PreconditionFailedException, BadRequestException
from flask import request

class Create(BaseCommand):
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        token = request.headers.get('Authorization')
        try:
            offer = Offer( \
                id = str(uuid.uuid4()), \
                postid = self.json_data["postId"], \
                description = self.json_data["description"], \
                size = self.json_data["size"], \
                fragile = self.json_data["fragile"], \
                offer = self.json_data["offer"], \
                userid = token.replace("Bearer ", "") \
            )                
        except: 
            raise BadRequestException()

        if offer.offer < 0 or offer.size not in ["SMALL", "MEDIUM", "LARGE"]:
            raise PreconditionFailedException()
        
        db.session.add(offer)
        db.session.commit()

        created_at = offer.createat

        if isinstance(created_at, tuple):
            created_at = created_at[0]

        new_offer = {
            "id": offer.id,
            "userId": offer.userid,
            "createdAt": created_at.isoformat()
        }

        return new_offer
