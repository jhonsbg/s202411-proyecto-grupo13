from flask_restful import Resource
from flask import request, make_response, jsonify
from modelos import db, User, UserSchema
from enum import Enum
import uuid

user_schema = UserSchema()

def enum_encoder(obj):
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError("Object of type {} is not JSON serializable".format(obj.__class__.__name__))

valid_tokens = set()

def generate_token():
    token = str(uuid.uuid4())
    valid_tokens.add(token)
    return token
    
class VistaUsers(Resource):
    def get(self):
        users = User.query.all()
        # Aplicar enum_encoder al campo 'size' en cada oferta antes de serializar
        for user in users:
            user.status = enum_encoder(user.status)
        
        # Serializar las ofertas utilizando Marshmallow
        serialized_users = [user_schema.dump(user) for user in users]
        return serialized_users
    
class VistaPing(Resource):
    def get(self):
        return "pong", 200
    
class VistaAuth(Resource):
    def post(self):

        if "username" in request.json or "password" in request.json: 
            return 400

        username = request.json["username"] 
        password = request.json["password"]
        
        if "wrong" in password or "fake" in username:
            return 404
        
        resp = {
            "id": 1,
            "token": generate_token(),
            "expireAt": "2024-03-20T14:28:23.382748"
        }
        
        return make_response(jsonify(resp), 200)
    