from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.routes import routes_blueprint
from .errors.errors import ApiError
from .models import db
import os

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/route_db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(os.environ.get('DB_USER'), \
                                                                    os.environ.get('DB_PASSWORD'), \
                                                                    os.environ.get('DB_HOST'), \
                                                                    os.environ.get('DB_PORT'), \
                                                                    os.environ.get('DB_NAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
app.register_blueprint(routes_blueprint)

db.create_all()

@app.errorhandler(ApiError)
def handle_exception(err):
    print("handle_exception")
    response = {
      "mssg": err.description
    }
    return jsonify(response), err.code

