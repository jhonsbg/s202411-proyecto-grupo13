from .base_command import BaseCommand
from ..models.offer import Offer, db
from ..errors.errors import BadRequestException, PermissionDeniedException, AuthenticationException, NotFoundException
from flask import request, jsonify, make_response, current_app
import uuid

class Delete(BaseCommand):
    def __init__(self):
        pass
    
    def execute(self, offer_id):

        if not self.is_valid_uuid(offer_id):
            raise BadRequestException()

        token = request.headers.get('Authorization')     
        
        try:
            if self.is_valid_token(token):
                offer = Offer.query.filter_by(id=offer_id).first()
                if not offer:
                    raise NotFoundException()

                db.session.delete(offer)
                db.session.commit()
                msg = {
                    "msg": "la oferta fue eliminada"
                }
                response = make_response(jsonify(msg), 200)
                return response
        except NotFoundException as e:
            raise NotFoundException()
        except Exception as e:
            return make_response(jsonify({"error": "Error interno del servidor"}), 500)

        
        if not token:
            raise PermissionDeniedException()
        
        if not self.is_valid_token(token):
            raise AuthenticationException()
        
    def is_valid_token(self, token):
        return token=="Bearer cd3d1303-2d62-4f60-8472-3349d34f690c"
    
    def is_valid_uuid(self, uuid_str):
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except ValueError:
            return False