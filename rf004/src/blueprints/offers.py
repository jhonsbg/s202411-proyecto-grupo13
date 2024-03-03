from flask import jsonify, request, Blueprint, make_response
from ..commands.autorizacion import Autorizacion
from ..models import OfferSchema
from ..commands.create import Create

offer_schema = OfferSchema()

offers_blueprint = Blueprint('posts', __name__)

@offers_blueprint.route('/rf004/posts/{id}/offers', methods = ['POST'])
def create():
    token = request.headers.get('Authorization') 
    user = Autorizacion(token).execute()
    return make_response(jsonify(Create(request.json, token, user['id'], id).execute()), 201)

@offers_blueprint.route('/rf004/ping', methods = ['GET'])
def ping():
    return 'pong'


