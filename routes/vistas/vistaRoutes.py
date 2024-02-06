from flask_restful import Resource
from flask import request, make_response, jsonify
from modelos import db, Route, RouteSchema
from datetime import datetime
import uuid
import logging

route_schema = RouteSchema()

valid_tokens = set()

def generate_token():
    token = str(uuid.uuid4())
    valid_tokens.add(token)
    return token

def is_valid_token(token):
    #return token in valid_tokens
    return token=="Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"

class VistaTokens(Resource):
    def get(self):
        token = generate_token()
        
        return jsonify({'token': token})


class VistaRoutes(Resource):
    
    def get(self):
        try:
            token = request.headers.get('Authorization')
            if not token:
                raise CustomPermissionDeniedException("No hay token en la solicitud")

            if not is_valid_token(token):
                raise CustomAuthenticationException("El token no es válido o está vencido")

            
            # GET /routes (Obtener todos los elementos)
            routes = Route.query.all()
            serialized_routes = [route_schema.dump(route) for route in routes]
            response = make_response(jsonify(serialized_routes), 200)
            return response

        except CustomAuthenticationException as e:
            error_message = 'El token no es válido o está vencido.'
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPermissionDeniedException as e:
            error_message = 'No hay token en la solicitud'
            response = make_response(jsonify(error_message), 403)
            return response
        except Exception as e:
            error_message = 'Error en la solicitud'
            response = make_response(jsonify(error_message), 500)
            return response
          
    def post(self):
        try:
            new_route = Route( \
            flightId = request.json["flightId"], \
            sourceAirportCode = request.json["sourceAirportCode"], \
            sourceCountry = request.json["sourceCountry"], \
            destinyAirportCode = request.json["destinyAirportCode"], \
            destinyCountry = request.json["destinyCountry"], \
            bagCost = request.json["bagCost"], \
            plannedStartDate = request.json["plannedStartDate"], \
            plannedEndDate = request.json["plannedEndDate"] \
            )
            token = request.headers.get('Authorization')
            
            if not token:
                raise CustomPermissionDeniedException("")

            if not is_valid_token(token):
                raise CustomAuthenticationException("")
        
            if is_valid_token(token):       
                resultado, mensaje = self.valida_fechas(new_route.plannedStartDate, new_route.plannedEndDate)
                if resultado:
                    existing_route = Route.query.filter_by(flightId=new_route.flightId).first()
                    if existing_route:
                        error_message = 'El flightId ya existe.' 
                        response = make_response(error_message, 412)
                    else:
                        db.session.add(new_route)
                        db.session.commit()
                        serialized_new_route = {
                            "id": new_route.id,
                            "createdAt": new_route.cupdateAt.isoformat()
                        }
                        response = make_response(jsonify(serialized_new_route), 201)
                else:
                    error_message = 'Las fechas del trayecto no son válidas' 
                    response = make_response(error_message, 412)
                return response
        except KeyError  as e:
            error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
            response = make_response(jsonify(error_message), 400)
            return response
        except CustomAuthenticationException as e:
            error_message = 'El token no es válido o está vencido.'
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPermissionDeniedException as e:
            error_message = 'No hay token en la solicitud'
            response = make_response(jsonify(error_message), 403)
            return response

    def valida_fechas(self, fecha_inicio, fecha_fin):
        try:

            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Verificar si las fechas están en el pasado
            if fecha_inicio < datetime.now() or fecha_fin < datetime.now():
                return False, "Las fechas no pueden estar en el pasado"

            # Verificar si las fechas son consecutivas
            if fecha_inicio >= fecha_fin:
                return False, "La fecha de inicio debe ser anterior a la fecha de fin"

            return True, "Fechas válidas"
        except ValueError:
            return False, "Formato de fecha incorrecto"

class VistaRoute(Resource):
    def get(self, id):
        try:
            token = request.headers.get('Authorization')
            if not token:
                raise CustomPermissionDeniedException("No hay token en la solicitud")

            if not is_valid_token(token):
                raise CustomAuthenticationException("El token no es válido o está vencido")
    
            # GET /routes/<id> (Obtener un elemento por ID)
            #Valida el uuid
            try:
                uuid.UUID(id)
            except ValueError:
                error_message = "El ID no es un UUID válido."
                response = make_response(jsonify(error_message), 400)
                return response
            
            existing_id = Route.query.get(id)
            if existing_id:
                    
                serialized_id = route_schema.dump(existing_id)
                response = make_response(jsonify(serialized_id), 200)
            else:
                error_message = 'El ID del trayecto no existe'
                response = make_response(error_message, 404)

            return response

        except CustomAuthenticationException as e:
            error_message = 'El token no es válido o está vencido.'
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPermissionDeniedException as e:
            error_message = 'No hay token en la solicitud'
            response = make_response(jsonify(error_message), 403)
            return response
        except Exception as e:
            error_message = 'Error en la solicitud'
            response = make_response(jsonify(error_message), 500)
            return response
        
    def delete(self, id):
        try:
            
            token = request.headers.get('Authorization')
            if not token:
                raise CustomPermissionDeniedException("No hay token en la solicitud")

            if not is_valid_token(token):
                raise CustomAuthenticationException("El token no es válido o está vencido")
    
            #Valida el uuid
            try:
                uuid.UUID(id)
            except ValueError:
                error_message = "El ID no es un UUID válido."
                response = make_response(jsonify(error_message), 400)
                return response
            
            existing_id = Route.query.get(id)
            if existing_id:
                db.session.delete(existing_id)
                db.session.commit()
                serialized_new_route = {
                    "msg": "el trayecto fue eliminado"
                }
                response = make_response(jsonify(serialized_new_route), 200)
            else:
                error_message = 'El ID del trayecto no existe'
                response = make_response(error_message, 404)

            return response

        except CustomAuthenticationException as e:
            error_message = 'El token no es válido o está vencido.'
            response = make_response(jsonify(error_message), 401)
            return response
        except CustomPermissionDeniedException as e:
            error_message = 'No hay token en la solicitud'
            response = make_response(jsonify(error_message), 403)
            return response
        except Exception as e:
            error_message = 'Error en la solicitud'
            response = make_response(jsonify(error_message), 500)
            return response
                         
class VistaReset(Resource):
    def post(self):
        routes = Route.query.all()

        for route in routes:
            db.session.delete(route)

        db.session.commit()
        return make_response("Todos los datos fueron eliminados", 200)
    
class VistaPing(Resource):
    def get(self):
       return make_response("pong", 200)
        
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
    
    

                            