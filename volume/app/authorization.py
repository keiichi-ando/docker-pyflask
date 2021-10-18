from flask import jsonify
from werkzeug.security import safe_str_cmp
from app.models import User

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401


def authenticate(username, password):
    user = _load_users().get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return _load_users().get(user_id, None)


def jwt_unauthorized_loader_handler(reason):
    return jsonify({'message': 'Unauthorized'}), HTTP_UNAUTHORIZED


def _load_users() -> dict:
    users = (
        User(1, 'sysuser', 'abcxyz.0'),
        User(2, 'guest', 'pass'),
    )
    return {u.username: u for u in _load_users()}
