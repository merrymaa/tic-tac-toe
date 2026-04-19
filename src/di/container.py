from datasource.model.storage import Storage
from datasource.repository.repository_impl import GameRepository
from datasource.repository.repository_backed_service import RepositoryBackedService
from datasource.database.database import init_db, SessionLocal
from datasource.database.user_repositort_impl import UserRepositoryImpl
from domain.service.user_service_impl import UserServiceImpl
from datasource.database.game_db_impl import GameDbImpl

class Container:
    def __init__(self):
        init_db()
        self.storage = Storage()
        self.repository = GameRepository(self.storage, SessionLocal)
        self.game_service = RepositoryBackedService(self.repository)
        self.user_repository = UserRepositoryImpl()
        self.user_service = UserServiceImpl(self.user_repository)
        self.user_bd_service = GameDbImpl()



container = Container()
