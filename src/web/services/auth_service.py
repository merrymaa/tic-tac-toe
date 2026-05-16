from sqlalchemy.sql.functions import user

from datasource.service.user_service_impl import UserServiceImpl
from web.model.jwt_provider import JwtProvider
from web.model.auth_dto import JwtRequest, JwtResponse

class AuthService:
    """"Сервис авторизации"""
    def __init__(self):
        self.user_service = UserServiceImpl()
        self.jwt_provider = JwtProvider()

    def authorize(self, jwt_request: JwtRequest) -> JwtResponse | None:

        user_uuid = self.user_service.authorize(jwt_request.login, jwt_request.password)
        if not user_uuid:
            return None

        access_token = self.jwt_provider.create_access_token(user_uuid)
        refresh_token = self.jwt_provider.create_refresh_token(user_uuid)

        return JwtResponse(
            accessToken = access_token,
            refreshToken = refresh_token)

    def refresh_access_token(self,  refresh_token: str) -> JwtResponse | None:

        user_uuid = self.jwt_provider.get_uuid_from_token(refresh_token)
        if not user_uuid:
            return None

        new_access_token = self.jwt_provider.create_access_token(user_uuid)

        return JwtResponse(
            type = "Bearer",
            accessToken=new_access_token,
            refreshToken=refresh_token)

    def refresh_refresh_token(self, refresh_token: str) -> JwtResponse | None:
        user_uuid = self.jwt_provider.get_uuid_from_token(refresh_token)
        if not user_uuid:
            return None

        new_access_token = self.jwt_provider.create_access_token(user_uuid)
        new_refresh_token = self.jwt_provider.create_refresh_token(user_uuid)

        return JwtResponse(
            type="Bearer",
            accessToken=new_access_token,
            refreshToken=new_refresh_token)
