from datasource.repository.repository_interface import Repository
from domain.model.game import CurrentGame
from datasource.model.storage import Storage
from datasource.mapper.mapper import Mapper


class GameRepository(Repository):
    """
    Реализация сервиса с использованием репозитория.
    """

    def __init__(self, storage: Storage):
        self._storage = storage

    def save(self, game: CurrentGame) -> None:
        """
        Преобразует Game в DTO.
        Сохраняет в хранилище.
        """
        game_dto = Mapper.from_domain_to_storage(game)
        self._storage.add(game_dto)

    def get(self, game_id) -> CurrentGame:
        """
        Извлекает DTO из хранилища.
        Преобразует DTO в domain с помощью маппера.
        """
        game_dto = self._storage.get(game_id)
        if game_dto is None:
            print(f"REPOSITORY: Игра {game_id} не найдена в хранилище")
            return None

        return Mapper.from_storage_to_domain(game_dto)
