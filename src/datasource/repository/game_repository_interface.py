from abc import ABC, abstractmethod
from domain.model.game import CurrentGame
from datasource.database.database import Games


class GameRepository(ABC):
    """
    Интерфейс репозитория игры.

    """
    @abstractmethod
    def save_game(self, game: CurrentGame) -> None:
        pass

    @abstractmethod
    def get_active_games(self) -> list:
        pass

    @abstractmethod
    def get_available_games(self, player_uuid: str) -> list[Games]:
        pass

