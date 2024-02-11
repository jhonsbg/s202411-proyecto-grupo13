from .base_command import BaseCommand
from ..models.offer import Offer
from flask import request, make_response, jsonify
from ..errors.errors import BadRequestException
from enum import Enum

class ListOffer(BaseCommand):
    def __init__(self):
        pass

    def execute(self):
        token = request.headers.get('Authorization')
        
        try:
            post = request.args.get("post",default="")
            owner = request.args.get("owner",default="")
            
            if not post and not owner:
                offers = Offer.query.all()
                serialized_offers = []

                for offer in offers:
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
                        
                    serialized_offers.append(serialized_offer)

                response = make_response(jsonify(serialized_offers), 200)
                return response
        
            elif post and not owner:
                offers = Offer.query.filter_by(postid=post).all()
                serialized_offers = []
                for offer in offers:
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
                    
                    serialized_offers.append(serialized_offer)

                response = make_response(jsonify(serialized_offers), 200)
                return response
            
            elif owner == 'me':
                serialized_offers = []
                user_id = token.replace("Bearer ", "") 
                offers = Offer.query.filter_by(userid=user_id).all()
                for offer in offers:
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
                        
                    serialized_offers.append(serialized_offer)

                response = make_response(jsonify(serialized_offers), 200)
                return response
            
            elif owner:
                serialized_offers = []
                offers = Offer.query.filter_by(userid=owner).all()
                for offer in offers:
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
                        
                    serialized_offers.append(serialized_offer)

                response = make_response(jsonify(serialized_offers), 200)
                return response 
                
        except KeyError as e:
            print(f"KeyError: {e}")
            error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
            response = make_response(jsonify(error_message), 400)
            return response
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise BadRequestException()
        
    def enum_encoder(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError("Object of type {} is not JSON serializable".format(obj.__class__.__name__))

    