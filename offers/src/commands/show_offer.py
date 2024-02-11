from .base_command import BaseCommand
from ..models.offer import Offer
from flask import make_response, jsonify
from ..errors.errors import NotFoundException
from enum import Enum
import uuid

class ShowOffer(BaseCommand):
    def __init__(self):
        pass

    def execute(self, offer_id):
        
        if not self.is_valid_uuid(offer_id) and offer_id != "ping":
            error_message = 'El id no es un valor string con formato uuid.'
            response = make_response(jsonify(error_message), 400)
            return response
        
        if offer_id == "ping":
            response = make_response("pong", 200)
            return response
        
        try:
            offer = Offer.query.filter_by(id=offer_id).first()
            
            if offer is None:
                raise NotFoundException()
            
            offer.size = self.enum_encoder(offer.size)

            serialized_offer = {
                "id": str(offer.id),
                "postId": offer.postid,
                "userId": offer.userid,
                "description": offer.description,
                "size": offer.size,
                "fragile": offer.fragile,
                "offer": offer.offer,
                "createdAt": offer.createat.isoformat()
            }
                    
            response = make_response(jsonify(serialized_offer), 200)
            return response
        except KeyError  as e:
            error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
            response = make_response(jsonify(error_message), 400)
            return response
        
    def enum_encoder(self,obj):
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError("Object of type {} is not JSON serializable".format(obj.__class__.__name__))
    
    def is_valid_uuid(self, uuid_str):
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except ValueError:
            return False
