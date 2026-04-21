from flask import Blueprint, jsonify, request
from flask_reqcheck import validate_body, get_valid_request
from di.container import container
from datasource.model.sign_up_request import SignUpRequest
import base64


auth_bp = Blueprint('auth_bp', __name__)


def decode_base(header: str):
    if not header or not header.startswith('Basic '):
        return None, None
    try:
        encoded = header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        login, password = decoded.split(':', 1)
        return login, password
    except Exception:
        return None, None


@auth_bp.route('/register', methods=['POST'])
@validate_body(SignUpRequest)
def register_user():
    validated_request = get_valid_request()
    success = container.user_service.register(validated_request.body)
    if success:
        return {"message": f"{validated_request.body.login} was successful registered"}, 201
    else:
        return {"error": "Login exists"}, 409


@auth_bp.route('/authorize', methods=['POST'])
def authorize_user():
    auth_header = request.headers.get('Authorization')
    login, password = decode_base(auth_header)
    if not login or not password:
        return jsonify({"error": "Invalid or missing Basic Auth header"}), 401

    user_uuid = container.user_service.authorize(login, password)
    if user_uuid is None:
        return jsonify({"error": "Authorization not success"}), 401
    return jsonify({"user_uuid": user_uuid}), 200




