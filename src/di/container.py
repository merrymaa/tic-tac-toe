from datasource.model.storage import Storage
from datasource.repository.repository_impl import GameRepository
from datasource.repository.repository_backed_service import RepositoryBackedService


class Container:
    def __init__(self):
        self.storage = Storage()
        self.repository = GameRepository(self.storage)
        self.game_service = RepositoryBackedService(self.repository)


container = Container()
