from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from os import environ

from modelos import db
from vistas import VistaUsers, VistaUser, VistaMe, VistaPing, VistaAuth, VistaReset

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/user_db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(environ.get('DB_USER'), \
                                                                    environ.get('DB_PASSWORD'), \
                                                                    environ.get('DB_HOST'), \
                                                                    environ.get('DB_PORT'), \
                                                                    environ.get('DB_NAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaUsers, '/users')
api.add_resource(VistaUser, '/users/<string:id_user>')
api.add_resource(VistaMe, '/users/me')
api.add_resource(VistaPing, '/users/ping')
api.add_resource(VistaAuth, '/users/auth')
api.add_resource(VistaReset, '/users/reset')