from flask import jsonify, request, Blueprint, make_response

from ..commands import Posts, Auth

import os

rf005_blueprint = Blueprint('rf005', __name__)


@rf005_blueprint.route('/rf005/posts/<post_id>', methods = ['GET'])
def posts(post_id):
    token = request.headers.get('Authorization')
    user = Auth(token).execute()
    return make_response(jsonify(Posts(user["id"], token, post_id).execute()), 200)

@rf005_blueprint.route('/rf005/ping', methods = ['GET'])
def ping():
    return 'pong'
