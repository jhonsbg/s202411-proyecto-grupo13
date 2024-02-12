from flask import Flask, jsonify, request, Blueprint, make_response
from ..models import Route, RouteSchema
from ..commands import Consulta
from ..commands import Create
from ..commands import Eliminar
from ..commands import VerFligth
from ..commands import Reset
from ..commands import Autorizacion


import os

route_schema = RouteSchema()

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/routes', methods = ['POST'])
def create():
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    #if  code == 200:
    return Create(request.json).execute()
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)

@routes_blueprint.route('/routes', methods = ['GET'])
def flight():
    token = request.headers.get('Authorization')
    flight_id = request.args.get('flight')
    code = Autorizacion(token).execute()
    #auth_info = Autorizacion(auth_token()).execute()
    #if  code == 200:
    return make_response(jsonify(VerFligth(flight_id).execute()), 200)
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)
    

@routes_blueprint.route('/routes/<string:id>', methods = ['GET'])
def consulta(id):
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    #if  code == 200:
    return make_response(jsonify(Consulta(id).execute()), 200)
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)


@routes_blueprint.route('/routes/<string:id>', methods = ['DELETE'])
def delete(id):
    token = request.headers.get('Authorization')
    code = Autorizacion(token).execute()
    #if  code == 200:
    return Eliminar(id).execute()
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code) 
    


@routes_blueprint.route('/routes/ping', methods = ['GET'])
def ping():
    return make_response("pong", 200)

@routes_blueprint.route('/routes/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return 'Todos los datos fueron eliminados'