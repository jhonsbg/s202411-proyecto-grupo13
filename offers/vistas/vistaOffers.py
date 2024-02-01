from flask_restful import Resource
from flask import request, make_response, jsonify
from modelos import db, Offer, OfferSchema
from enum import Enum
import uuid

offer_schema = OfferSchema()

def enum_encoder(obj):
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError("Object of type {} is not JSON serializable".format(obj.__class__.__name__))

valid_tokens = set()

def generate_token():
    token = str(uuid.uuid4())
    valid_tokens.add(token)
    return token

def is_valid_token(token):
    #return token in valid_tokens
    return token=="Bearer cd3d1303-2d62-4f60-8472-3349d34f690c"

class VistaTokens(Resource):
    def get(self):
        token = generate_token()
        
        return jsonify({'token': token})
    
class VistaOffers(Resource):
    def get(self):
        try:
            post = request.args.get("post", default="")
            owner = request.args.get("owner", default="")
            # Aplicar enum_encoder al campo 'size' en cada oferta antes de serializar
            if post != "" and owner != "":
                offers = Offer.query.filter_by(postid=post, userid=owner).all()
                # Aplicar enum_encoder al campo 'size' en cada oferta antes de serializar
                for offer in offers:
                    offer.size = enum_encoder(offer.size)
                # Serializar las ofertas utilizando Marshmallow
                serialized_offers = [offer_schema.dump(offer) for offer in offers]
            else:
                offers = Offer.query.all()
                # Aplicar enum_encoder al campo 'size' en cada oferta antes de serializar
                for offer in offers:
                    offer.size = enum_encoder(offer.size)
                # Serializar las ofertas utilizando Marshmallow
                serialized_offers = [offer_schema.dump(offer) for offer in offers]
            
            response = make_response(jsonify(serialized_offers), 200)
            return response
        
        except CustomAuthenticationException as e:
            error_message = 'El token no es válido o está vencido.'
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPermissionDeniedException as e:
            error_message = 'No hay token en la solicitud'
            response = make_response(jsonify(error_message), 403)
            return response
        except KeyError  as e:
            error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
            response = make_response(jsonify(error_message), 400)
            return response  
        
    def post(self):
        try:
            new_offer = Offer( \
                postid = request.json["postId"], \
                description = request.json["description"], \
                size = request.json["size"], \
                fragile = request.json["fragile"], \
                offer = request.json["offer"] \
            )

            token = request.headers.get('Authorization')

            if not token:
                raise CustomPermissionDeniedException("")

            if not is_valid_token(token):
                raise CustomAuthenticationException("")
            
            if is_valid_token(token):   
                if new_offer.offer < 0 or new_offer.size not in ["SMALL", "MEDIUM", "LARGE"]:
                    raise CustomPreconditionFailedException("")
            
            db.session.add(new_offer)
            db.session.commit()
            
            # Asegúrate de que createat sea un objeto datetime
            created_at = new_offer.createat

            if isinstance(created_at, tuple):
                created_at = created_at[0]

            serialized_new_offer = {
                "id": new_offer.id,
                "userId": new_offer.userid,
                "createdAt": created_at.isoformat()
            }

            response = make_response(jsonify(serialized_new_offer), 201)
            return response
        except KeyError  as e:
            error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
            response = make_response(jsonify(error_message), 400)
            return response
        except CustomPermissionDeniedException as e:
            error_message = 'No hay token en la solicitud'
            response = make_response(jsonify(error_message), 403)
            return response
        except CustomAuthenticationException as e:
            error_message = 'El token no es válido o está vencido.'
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPreconditionFailedException as e:
            error_message = 'En el caso que los valores no estén entre lo esperado, por ejemplo el tamaño del paquete no sea válido, o la oferta sea negativa.'
            response = make_response(jsonify(error_message), 412)
            return response
    
class CustomPermissionDeniedException(Exception):
    def __init__(self, message="Permission denied"):
        self.message = message
        super().__init__(self.message)

class CustomAuthenticationException(Exception):
    def __init__(self, message="Token invalid"):
        self.message = message
        super().__init__(self.message)

class CustomPreconditionFailedException(Exception):
    def __init__(self, message="values out range or values incorrect"):
        self.message = message
        super().__init__(self.message)

class VistaReset(Resource):
    def post(self):
        offers = Offer.query.all()

        for offer in offers:
            db.session.delete(offer)

        db.session.commit()
        return make_response("Todos los datos fueron eliminados", 200)



    