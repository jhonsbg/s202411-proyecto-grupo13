from flask import Flask, jsonify, request, Blueprint, make_response
from ..models import Score, ScoreSchema
from ..commands import Consulta
from ..commands import Calcula
from ..commands import Reset
from ..commands import Autorizacion


import os

score_schema = ScoreSchema()

scores_blueprint = Blueprint('scores', __name__)

@scores_blueprint.route('/scores', methods = ['POST'])
def calcula():
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    return Calcula(request.json).execute()

@scores_blueprint.route('/scores', methods = ['GET'])
def consulta():
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    return make_response(jsonify(Consulta(request.json).execute()), 200)

@scores_blueprint.route('/scores/ping', methods = ['GET'])
def ping():
    return make_response("pong", 200)

@scores_blueprint.route('/scores/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return 'Todos los datos fueron eliminados'