from flask import jsonify, request, Blueprint, make_response
from ..commands.autorizacion import Autorizacion
from ..models import OfferSchema
from ..commands.create import Create
from ..commands.delete import Delete
from ..commands.list_offer import ListOffer
from ..commands.reset import Reset
from ..commands.show_offer import ShowOffer

offer_schema = OfferSchema()

offers_blueprint = Blueprint('offers', __name__)

@offers_blueprint.route('/offers', methods = ['POST'])
def create():
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    #if  code == 200:
    return make_response(jsonify(Create(request.json).execute()), 201)
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)

@offers_blueprint.route('/offers', methods = ['GET'])
def listOffer():
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    #if  code == 200:
    return ListOffer().execute()
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)

@offers_blueprint.route('/offers/<offer_id>', methods = ['GET'])
def show(offer_id):
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    #if  code == 200:
    return ShowOffer().execute(offer_id)
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)
    
@offers_blueprint.route('/offers/ping', methods = ['GET'])
def ping():
    return ShowOffer().execute('ping')

@offers_blueprint.route('/offers/<offer_id>', methods = ['DELETE'])
def delete(offer_id):
    token = request.headers.get('Authorization') 
    code = Autorizacion(token).execute()
    #if  code == 200:
    return Delete().execute(offer_id)
    #else:
    #    return make_response(jsonify({"error": "Unauthorized"}), code)

@offers_blueprint.route('/offers/reset', methods = ['POST'])
def reset():
    return Reset().execute()

