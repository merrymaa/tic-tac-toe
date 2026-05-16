import base64
from functools import wraps
from flask import request, jsonify, g
from di.container import container
from web.model.jwt_provider import JwtProvider


class UserAuthenticator:
    @staticmethod
    def decode_base(header: str):
        if not header or not header.startswith('Basic '):
            return None, None
        try:
            encoded = header.split(' ')[1]
            decoded = base64.b64decode(encoded).decode('utf-8')
            login, password = decoded.split(':', 1)
            return login, password
        except Exception as e:
            print(f"Error in UserAuthenticator.decode_base - {e}")
            return None, None

    # @staticmethod
    # def protected(route_function):
    #     @wraps(route_function)
    #     def wrapper(*args, **kwargs):
    #         try:
    #             auth_header = request.headers.get('Authorization')
    #             login, password = UserAuthenticator.decode_base(auth_header)
    #             if not login or not password:
    #                 return jsonify({"error": "Missing or invalid Authorization header"}), 401
    #
    #             user_uuid = container.user_service.authorize(login, password)
    #             if user_uuid is None:
    #                 return jsonify({"error": "Invalid credentials"}), 401
    #
    #             kwargs['user_uuid'] = user_uuid
    #             return route_function(*args, **kwargs)
    #         except Exception as e:
    #             print(f"Error in decorate authentication - {e}")
    #             return jsonify({"error": "Internal server error during authentication"}), 500
    #     return wrapper

    @staticmethod
    def extract_token() -> str | None:
        """"Извлекает токен типа Bearer из заголовка"""
        header = request.headers.get('Authorization')
        if not header:
            return None
        header_split = header.split(' ')
        if header_split[0].lower() != 'bearer' or len(header_split) != 2:
            return None
        return header_split[1]

    @staticmethod
    def my_jwt_required(route_func):
        @wraps(route_func)
        def wrapper(*args, **kwargs):
            token = UserAuthenticator.extract_token()
            if not token:
                return jsonify({"msg": "Missing Authorization Header"}), 401
            if not JwtProvider.validate_access_token(token):
                return jsonify({"msg": "Invalid or expired token"}), 401
            user_uuid = JwtProvider.get_uuid_from_token(token)
            if not user_uuid:
                return jsonify({"msg": "Invalid token claims"}), 401
            g.user_uuid = user_uuid
            return route_func(*args, **kwargs)
        return wrapper

