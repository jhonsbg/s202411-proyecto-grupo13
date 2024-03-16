from flask import jsonify, request, Blueprint, make_response
from ..commands.autorizacion import Autorizacion
from ..models import CardSchema
from ..commands.create import Create
from ..commands.list_card import ListCard
from ..commands.reset import Reset

card_schema = CardSchema()

cards_blueprint = Blueprint('cards', __name__)

@cards_blueprint.route('/credit-cards', methods = ['POST'])
def create():
    token = request.headers.get('Authorization') 
    user = Autorizacion(token).execute()
    print(user)
    return make_response(jsonify(Create(request.json, token, user['id']).execute()), 201)

@cards_blueprint.route('/credit-cards', methods = ['GET'])
def listCard():
    token = request.headers.get('Authorization') 
    user = Autorizacion(token).execute()
    return ListCard(token, user['id']).execute()

@cards_blueprint.route('/credit-cards/ping', methods = ['GET'])
def ping():
    return 'pong'

@cards_blueprint.route('/credit-cards/reset', methods = ['POST'])
def reset():
    return Reset().execute()