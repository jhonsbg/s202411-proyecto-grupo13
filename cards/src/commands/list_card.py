from .base_command import BaseCommand
from ..models.card import Card, CardSchema
from flask import request, make_response, jsonify
from ..errors.errors import BadRequestException
from enum import Enum

card_schema = CardSchema()

class ListCard(BaseCommand):
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def execute(self):
        if self.user_id is None:
            error_message = 'El usuario no tiene tarjetas asociadas.'
            response = make_response(jsonify(error_message), 400)
            return response
        
        cards = Card.query.filter_by(userId=self.user_id).all()
        try:
            if cards is not None and len(cards) > 0:
                # for card in cards:
                #     card.status = card.status
                #     print(card.status.value)
                response = make_response(jsonify([card_schema.dump(card) for card in cards]), 200)
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
            print(54)
            print(f"Unexpected error: {e}")
            raise BadRequestException()
        