from .base_command import BaseCommand
from ..models.card import Card
from flask import request, make_response, jsonify
from ..errors.errors import BadRequestException
from enum import Enum

class ListCard(BaseCommand):
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def execute(self):
        if self.user_id is None:
            error_message = 'El usuario no tiene tarjetas asociadas.'
            response = make_response(jsonify(error_message), 400)
            return response
        
        cards = Card.query.filter_by(userid=self.user_id).all()
        try:
            if cards is not None and len(cards) > 0:
                serialized_cards = []
                for card in cards:
                    serialized_card = {
                        "id": str(card.id),
                        "token": card.token,
                        "userId": card.userid,
                        "lastFourDigits": card.lastFourDigits,
                        "issuer": card.issuer,
                        "status": card.status,
                        "createdAt": card.createat.isoformat(),
                        "updatedAt": card.updateat.isoformat()
                    }
                    serialized_cards.append(serialized_card)
                response = make_response(jsonify(serialized_cards), 200)
                return response
            
            else:
                error_message = 'El usuario no tiene tarjetas asociadas.'
                response = make_response(jsonify(error_message), 400)
                return response
                            
        except KeyError as e:
            print(f"KeyError: {e}")
            error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
            response = make_response(jsonify(error_message), 400)
            return response
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise BadRequestException()
        