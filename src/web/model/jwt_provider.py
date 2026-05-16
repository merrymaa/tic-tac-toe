from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from web.model.auth_dto import JwtRequest, JwtResponse
from flask import request


class JwtProvider:

    @staticmethod
    def create_access_token(user_uuid: str) -> str:
        return create_access_token(identity=user_uuid)

    @staticmethod
    def create_refresh_token(user_uuid: str) -> str:
        return create_refresh_token(identity=user_uuid)

    @staticmethod
    def validate_access_token(access_token: str) -> bool:
        try:
            decoded = decode_token(access_token, allow_expired=False)
            if decoded.get('type') != 'access':
                return False
            return True
        except Exception as e:
            print(f"Access token validation error: {e}")
            return False

    @staticmethod
    def validate_refresh_token(refresh_token: str) -> bool:
        try:
            decoded = decode_token(refresh_token, allow_expired=False)
            if decoded.get('type') != 'refresh':
                return False
            return True
        except Exception as e:
            print(f"Refresh token validation error: {e}")
            return False

    @staticmethod
    def get_uuid_from_token(token: str) -> str | None:
        try:
            decoded = decode_token(token, allow_expired=False)
            return decoded.get("sub")
        except Exception as e:
            return None


