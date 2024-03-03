from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.rf005 import rf005_blueprint
from .errors.errors import ApiError
import os

app = Flask(__name__)


app_context = app.app_context()
app_context.push()

app.register_blueprint(rf005_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    print("handle_exception")
    response = {
      "mssg": err.description
    }
    return jsonify(response), err.code

