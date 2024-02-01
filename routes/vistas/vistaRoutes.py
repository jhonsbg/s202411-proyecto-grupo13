from flask_restful import Resource
from flask import request, make_response, jsonify
from modelos import db, Route, RouteSchema

route_schema = RouteSchema()


class VistaRoutes(Resource):
    
    def post(self):
                     
                error_message = 'En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.'
                response = make_response(jsonify(error_message), 400)
                return response

                            