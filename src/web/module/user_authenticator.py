import base64
from functools import wraps
from flask import request, jsonify
from di.container import container

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
        except Exception:
            return None, None

    @staticmethod
    def protected(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            login, password = UserAuthenticator.decode_base(auth_header)
            if not login or not password:
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            user_uuid = container.user_service.authorize(login, password)
            if user_uuid is None:
                return jsonify({"error": "Invalid credentials"}), 401

            kwargs['user_uuid'] = user_uuid
            return route_function(*args, **kwargs)
            # return route_function()
        return wrapper
