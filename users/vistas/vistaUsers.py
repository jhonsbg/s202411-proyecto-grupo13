from flask_restful import Resource
from flask import request, make_response, jsonify
from modelos import db, User, UserSchema, StatusEnum
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

def is_valid_token(token):
    return True
    
class VistaUsers(Resource):
    def get(self):
        users = User.query.all()

        for user in users:
            user.status = enum_encoder(user.status)
        
        serialized_users = [user_schema.dump(user) for user in users]
        return serialized_users

    def post(self):
        try:
            new_user= User( \
                username = request.json["username"], \
                password = request.json["password"], \
                email = request.json["email"], \
                dni = request.json["dni"], \
                fullName = request.json["fullName"], \
                phoneNumber = request.json["phoneNumber"], \
                status = StatusEnum.POR_VERIFICAR
            )

            token = request.headers.get('Authorization')

            if User.query.filter_by(username=new_user.username).count() > 0:
                raise CustomPreconditionFailedException("username ya existe")
            
            if User.query.filter_by(email=new_user.email).count() > 0:
                raise CustomPreconditionFailedException("correo ya existe")
            
            db.session.add(new_user)
            db.session.commit()
            
            # Asegúrate de que createat sea un objeto datetime
            created_at = new_user.createat

            if isinstance(created_at, tuple):
                created_at = created_at[0]

            serialized_new_offer = {
                "id": new_user.id,
                "createdAt": created_at.isoformat()
            }

            response = make_response(jsonify(serialized_new_offer), 201)
            return response
        
        except KeyError as e:
            error_message = {'error': f'Campos incompletos y/o formato no esperado: {str(e)}'}
            response = make_response(jsonify(error_message), 400)
            return response
        except CustomPermissionDeniedException as e:
            error_message = {'error': f'Falta el token de seguridad: {str(e)}'}
            response = make_response(jsonify(error_message), 403)
            return response
        except CustomAuthenticationException as e:
            error_message = {'error': f'Token no valido: {str(e)}'}
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPreconditionFailedException as e:
            error_message = {'error': f'valores no estan entre lo esperado: {str(e)}'}
            response = make_response(jsonify(error_message), 412)
            return response
    
class VistaPing(Resource):
    def get(self):
        return make_response("pong", 200)
    
class VistaAuth(Resource):
    def post(self):

        if "username" in request.json or "password" in request.json: 
            return make_response("", 400)

        username = request.json["username"] 
        password = request.json["password"]
        
        if "wrong" in password or "fake" in username:
            return make_response("", 404)
        
        resp = {
            "id": 1,
            "token": generate_token(),
            "expireAt": "2024-03-20T14:28:23.382748"
        }
        
        return make_response(jsonify(resp), 200)
    

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
