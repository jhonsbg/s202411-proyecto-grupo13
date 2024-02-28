from flask import Flask, jsonify, request, Blueprint

from ..commands.create_post import CreatePost
from ..commands.get_post import GetPost
from ..commands.get_posts import GetPosts
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset
# from ..commands.create_post_public import CreatePostPublic
from ..commands.delete_post import DeletePost

posts_blueprint = Blueprint('posts', __name__)

@posts_blueprint.route('/posts', methods = ['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    post = CreatePost(request.get_json(), auth_info['id']).execute()
    return jsonify(post), 201

@posts_blueprint.route('/posts', methods = ['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    posts = GetPosts(request.args.to_dict(), auth_info['id']).execute()
    return jsonify(posts)

@posts_blueprint.route('/posts/<id>', methods = ['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    post = GetPost(id).execute()
    return jsonify(post)

@posts_blueprint.route('/posts/<id>', methods = ['DELETE'])
def delete(id):
    Authenticate(auth_token()).execute()
    post = DeletePost(id).execute()
    return jsonify({"msg": "la publicación fue eliminada"}), 200

@posts_blueprint.route('/posts/ping', methods = ['GET'])
def ping():
    return 'pong'

@posts_blueprint.route('/posts/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization


# @posts_blueprint.route('/public/posts', methods = ['POST'])
# def createPublic():
#     auth_info = Authenticate(auth_token()).execute()
#     token = request.headers['Authorization']
#     post = CreatePostPublic(request.get_json(), auth_info['id'],token).execute()
#     return jsonify(post), 201