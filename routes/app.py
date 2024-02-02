from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from os import environ

from modelos import db, Route
from vistas import vistaRoutes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/routes_db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()


db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(vistaRoutes, '/routes')

