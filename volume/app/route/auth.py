from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity
from os import path
import json
import settings
from app.helpers import is_json

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login() -> tuple:
    if is_json(request.get_data()) == False:
        body = {'statusCode': HTTP_BAD_REQUEST, 'message': 'Missing JSON in request'}
        return jsonify(body), HTTP_BAD_REQUEST

    _request_body = json.loads(request.get_data())
    if not _request_body.keys() >= {'name', 'password'}:
        body = {'statusCode': HTTP_BAD_REQUEST, 'message': 'Missing name or password in request'}
        return jsonify(body), HTTP_BAD_REQUEST

    _auth_user = None
    for _user in get_all_users():
        _is_match_name = _user['name'] == _request_body['name']
        _is_match_pass = _user['password'] == _request_body['password']
        if _is_match_name and _is_match_pass:
            _auth_user = _user
            break

    if _auth_user is None:
        body = {'statusCode': HTTP_UNAUTHORIZED, 'message': 'Login failure. Bad name or password'}
        return jsonify(body), HTTP_UNAUTHORIZED

    _token = create_access_token(identity=_auth_user['name'])
    body = {'message': 'Login succeeded', 'username': _auth_user['name'], 'access_token': _token, 'team': _auth_user['team']}
    return jsonify(body), HTTP_OK


@auth.route('/logout')
@jwt_required()
def logout() -> tuple:
    return jsonify({"message": "logout successful"}), HTTP_OK


@auth.route('/users', methods=['GET'])
@jwt_required()
def index() -> tuple:
    _current_user = get_jwt_identity()
    return jsonify({'login_user': _current_user, 'users': get_all_users()}), HTTP_OK


def jwt_unauthorized_loader_handler(reason) -> tuple:
    return jsonify({'statusCode': HTTP_UNAUTHORIZED, 'message': 'Unauthorized'}), HTTP_UNAUTHORIZED


def get_all_users() -> dict:
    """認証用ユーザーデータ取得
    Returns:
        dict: [description]
    """
    _filename = path.abspath(path.join(settings.APP_PATH, 'data', f'users.json'))
    if path.exists(_filename) == False:
        return {}
    return json.loads(open(_filename, encoding='UTF-8').read())['data']
