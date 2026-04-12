from datasource.model.storage import Storage
from datasource.repository.repository_impl import GameRepository
from datasource.repository.repository_backed_service import RepositoryBackedService
from datasource.database.database import init_db, SessionLocal


class Container:
    def __init__(self):
        init_db()
        self.storage = Storage()
        self.repository = GameRepository(self.storage, SessionLocal)
        self.game_service = RepositoryBackedService(self.repository)


container = Container()
