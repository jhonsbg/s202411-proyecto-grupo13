from flask import jsonify, request, Blueprint, make_response
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
    return make_response(jsonify(Create(request.json).execute()), 201)

@offers_blueprint.route('/offers', methods = ['GET'])
def listOffer():
    return ListOffer().execute()

@offers_blueprint.route('/offers/<offer_id>', methods = ['GET'])
def show(offer_id):
    return ShowOffer().execute(offer_id)

@offers_blueprint.route('/offers/<offer_id>', methods = ['DELETE'])
def delete(offer_id):
    return Delete().execute(offer_id)

@offers_blueprint.route('/offers/reset', methods = ['POST'])
def reset():
    return Reset().execute()

