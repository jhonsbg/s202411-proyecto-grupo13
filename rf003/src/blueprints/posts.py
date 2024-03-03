from flask import jsonify, request, Blueprint, make_response
from ..commands.autorizacion import Autorizacion
from ..models import PostSchema
from ..commands.create import Create

post_schema = PostSchema()

posts_blueprint = Blueprint('posts', __name__)

@posts_blueprint.route('/rf003/posts', methods = ['POST'])
def create():
    token = request.headers.get('Authorization') 
    user = Autorizacion(token).execute()
    return make_response(jsonify(Create(request.json, token, user['id']).execute()), 201)

