from datasource.service.user_service_impl import UserServiceImpl
from datasource.database.database import init_db
from domain.service.game_service_imp import GameServiceMinimax
from datasource.repository.repository_backed_service import RepositoryBackedService


class Container:
    def __init__(self):
        init_db()

        self.game_service = RepositoryBackedService()
        self.user_service = UserServiceImpl()


container = Container()
