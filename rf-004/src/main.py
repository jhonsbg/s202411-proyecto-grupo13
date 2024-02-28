import json
from flask import Flask, Response, jsonify
from .session import Session, engine
from .models.model import Base
from .blueprints.posts import posts_blueprint
from .errors.errors import ApiError

app = Flask(__name__)
app.register_blueprint(posts_blueprint)

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description 
    }
    response_json = json.dumps(response, ensure_ascii=False)
    return Response(response_json, content_type='application/json; charset=utf-8'), err.code