from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.offers import posts_blueprint
from .errors.errors import ApiError

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

app.register_blueprint(posts_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    print("handle_exception")
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code