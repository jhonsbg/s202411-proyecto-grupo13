from flask import Flask, jsonify, request, Blueprint, make_response
from ..models import StatusEnum, User, UserSchema
from ..commands import Reset
from ..commands import Create
from ..commands import Edit
from ..commands import Me
from ..commands import Auth

import os

user_schema = UserSchema()

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods = ['POST'])
def create():
    new_user = User( \
        username = request.json["username"], \
        password = request.json["password"], \
        email = request.json["email"], \
        dni = request.json["dni"], \
        fullName = request.json["fullName"], \
        phoneNumber = request.json["phoneNumber"], \
        status = StatusEnum.POR_VERIFICAR
    )
    return make_response(jsonify(Create(new_user).execute()), 201)

@users_blueprint.route('/users/<string:id_user>', methods = ['PATCH'])
def edit(id_user):
    Edit(id_user, request.json).execute()

    response = {
        "msg": "el usuario ha sido actualizado"
    }

    return make_response(jsonify(response), 200)

@users_blueprint.route('/users/me', methods = ['GET'])
def me():
    token = request.headers.get('Authorization')
    return make_response(user_schema.dump(Me(token).execute()), 200)

@users_blueprint.route('/users/ping', methods = ['GET'])
def ping():
    return 'pong'

@users_blueprint.route('/users/auth', methods = ['POST'])
def auth():
    return make_response(jsonify(Auth(request.json).execute()), 200)

@users_blueprint.route('/users/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return 'Todos los datos fueron eliminados'