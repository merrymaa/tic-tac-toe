from urllib import response

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flask_reqcheck import validate_body, get_valid_request
from di.container import container
from datasource.model.sign_up_request import SignUpRequest
import base64

from web.model.auth_dto import JwtRequest

auth_bp = Blueprint('auth_bp', __name__)


# def decode_base(header: str):
#     if not header or not header.startswith('Basic '):
#         return None, None
#     try:
#         encoded = header.split(' ')[1]
#         decoded = base64.b64decode(encoded).decode('utf-8')
#         login, password = decoded.split(':', 1)
#         return login, password
#     except Exception as e:
#         print(f"Error decode Basic Auth: {e}")
#         return None, None


@auth_bp.route('/authorize', methods=['POST'])
def authorize():
    username = request.json.get("login", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"Error": "Bad user name or password"}), 401

    jwt_request = JwtRequest(login=username, password=password)
    jwt_response = container.auth_service.authorize(jwt_request)

    if not jwt_response:
        return jsonify({"error": "User not authorised"}), 401

    return jsonify({
        "type": jwt_response.type,
        "accessToken": jwt_response.accessToken,
        "refreshToken": jwt_response.refreshToken
    }), 200

@auth_bp.route('/refresh_access_token', methods=['POST'])
def refresh_access_token():
    refresh_token = request.json.get("refresh_token", None)
    if not refresh_token:
        return jsonify({"Error": "Invalid or expired refresh token"}), 400

    jwt_response = container.auth_service.refresh_access_token(refresh_token)
    if not jwt_response:
        return jsonify({"Error": "Invalid or expired refresh token"}), 401


    return jsonify({
        "type": jwt_response.type,
        "accessToken": jwt_response.accessToken,
        "refreshToken": jwt_response.refreshToken
    }), 200

@auth_bp.route('/refresh_refresh_token', methods=['POST'])
def refresh_refresh_token():
    refresh_token = request.json.get("refresh_token", None)
    if not refresh_token:
        return jsonify({"Error": "Invalid or expired refresh token"}), 400

    jwt_response = container.auth_service.refresh_refresh_token(refresh_token)
    if not jwt_response:
        return jsonify({"Error": "Invalid or expired refresh token"}), 401

    return jsonify({
        "type": jwt_response.type,
        "accessToken": jwt_response.accessToken,
        "refreshToken": jwt_response.refreshToken
    }), 200



@auth_bp.route('/register', methods=['POST'])
@validate_body(SignUpRequest)
def register_user():
    try:
        validated_request = get_valid_request()

        success = container.user_service.register(validated_request.body)
        if success:
            return {"message": f"{validated_request.body.login} was successful registered"}, 201
        else:
            return {"error": "Login exists"}, 409

    except Exception as e:
        return {"error": f"Internal server error during registration - {e}"}, 500


# @auth_bp.route('/authorize', methods=['POST'])
# def authorize_user():
#     try:
#         auth_header = request.headers.get('Authorization')
#         login, password = decode_base(auth_header)
#         if not login or not password:
#             return jsonify({"error": "Invalid or missing Basic Auth header"}), 401
#
#         user_uuid = container.user_service.authorize(login, password)
#         if user_uuid is None:
#             return jsonify({"error": "Authorization not success"}), 401
#         return jsonify({"user_uuid": user_uuid}), 200
#     except Exception as e:
#         print(f"Error in authorization: {e}")
#         return jsonify({"error": "Internal server error during authorization"}), 500


