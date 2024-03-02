from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.scores import scores_blueprint
from .errors.errors import ApiError
from .models import db
import os

app = Flask(__name__)

if os.environ.get('TESTING') is not None and bool(os.environ.get('TESTING')): 
  basedir = os.path.abspath(os.path.dirname(__file__))
  app.config['SQLALCHEMY_DATABASE_URI'] =\
      'sqlite:///' + os.path.join(basedir, 'test_database.db')
else:
  #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/score_db"
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
db.create_all()

app.register_blueprint(scores_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    print("handle_exception")
    response = {
      "mssg": err.description
    }
    return jsonify(response), err.code