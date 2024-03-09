import uuid
from .base_command import BaseCommand
from ..models.card import Card, db
from ..errors.errors import BadRequestException
from flask import request

class Create(BaseCommand):
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        token = request.headers.get('Authorization')
        try:
            card = Card( \
                id = str(uuid.uuid4()), \
                token = self.json_data['token'], \
                userid = self.json_data['userId'], \
                lastFourDigits = self.json_data['lastFourDigits'], \
                ruv = self.json_data['ruv'], \
                issuer = self.json_data['issuer'], \
                status = self.json_data['status']                
            )
                         
        except: 
            raise BadRequestException()
        
        db.session.add(card)
        db.session.commit()

        created_at = card.createat

        if isinstance(created_at, tuple):
            created_at = created_at[0]

        new_card = {
            "id": card.id,
            "userId": card.userid,
            "createdAt": created_at.isoformat()
        }

        return new_card
