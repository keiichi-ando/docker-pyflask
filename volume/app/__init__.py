from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from os import path, getenv
from datetime import timedelta
import logging.config
import json

from app.route.auth import jwt_unauthorized_loader_handler


def create_app():

    # logger setup load
    _logconfig = path.join(path.abspath(path.dirname(__file__)), 'logconfig.json')
    _json = json.loads(open(_logconfig, encoding='UTF-8').read())
    logging.config.dictConfig(_json)

    app = Flask(__name__, static_folder='../src/dist/static')

    app.secret_key = getenv('SEACRET_KEY', '')
    app.config['JSON_AS_ASCII'] = False
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)

    CORS(app)

    jwt = JWTManager(app)
    jwt.unauthorized_loader(jwt_unauthorized_loader_handler)

    # blueprint for auth routes in our app
    from .route.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')

    # blueprint for frontend
    from .route.http import http as http_blueprint
    app.register_blueprint(http_blueprint)

    return app
