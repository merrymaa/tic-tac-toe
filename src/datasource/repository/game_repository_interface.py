from abc import ABC, abstractmethod
from domain.model.game import CurrentGame
from datasource.database.database import Games, User


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

    @abstractmethod
    def get_finished_games(self, user_uuid: str) -> list[Games]:
        pass

    @abstractmethod
    def get_current_game(self, game_uuid: str) -> Games:
        pass

    @abstractmethod
    def get_user(self, user_uuid: str) -> User:
        pass

    @abstractmethod
    def get_game(self, game_uuid: str) -> CurrentGame:
        pass

    @abstractmethod
    def get_statistic(self, n: int) -> dict:
        pass
