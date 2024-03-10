import uuid
from .base_command import BaseCommand
from ..models.card import Card, db
from ..errors.errors import BadRequestException
from flask import request

class Create(BaseCommand):
    def __init__(self, json_data, token, user_id):
        self.json_data = json_data
        self.token = token
        self.user_id = user_id

    def execute(self):
        try:
            card = Card( \
                id = str(uuid.uuid4()), \
                token = self.token, \
                userid = self.user_id, \
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
