from datasource.service.user_service_impl import UserServiceImpl
from datasource.database.database import init_db
from datasource.repository.repository_backed_service import RepositoryBackedService
from web.model.jwt_provider import JwtProvider
from web.services.auth_service import AuthService

class Container:
    def __init__(self):
        init_db()

        self.game_service = RepositoryBackedService()
        self.user_service = UserServiceImpl()
        self.jwt_provider = JwtProvider()
        self.auth_service = AuthService()


container = Container()
