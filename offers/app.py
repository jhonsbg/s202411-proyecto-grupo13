from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from os import environ

from modelos import db
from vistas import VistaOffers, VistaTokens, VistaReset, VistaOffer, VistaPing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaOffers, '/offers')
api.add_resource(VistaOffer, '/offers/<string:id>')
api.add_resource(VistaReset, '/offers/reset')
api.add_resource(VistaPing, '/offers/ping')
api.add_resource(VistaTokens, '/generar_token')