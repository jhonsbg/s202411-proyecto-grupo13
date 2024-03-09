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
                title = self.json_data["title"], \
                description = self.json_data["description"], \
                price = self.json_data["price"], \
                location = self.json_data["location"], \
                delivery = self.json_data["delivery"], \
                userid = token.replace("Bearer ", "") \
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
