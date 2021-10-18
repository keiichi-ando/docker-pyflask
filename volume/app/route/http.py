from flask import Blueprint, request, send_from_directory
from flask.helpers import NotFound
from flask.wrappers import Response
from logging import getLogger

http = Blueprint('http', __name__)


@http.after_request
def after_request(response):
    getLogger().info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@http.route('/', defaults={'filename': ''})
@http.route('/<path:filename>')
def index(filename: str) -> Response:
    try:
        return send_from_directory('../src/dist', filename)
    except NotFound:
        return send_from_directory('../src/dist', 'index.html')
