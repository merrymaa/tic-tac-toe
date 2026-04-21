from abc import ABC, abstractmethod
from domain.model.game import CurrentGame


class GameRepository(ABC):
    """
    Интерфейс репозитория игры.

    """

    def save_game(self, game: CurrentGame) -> None:
        pass

    @staticmethod
    def get_active_games(self) -> list:
        pass

    # @abstractmethod
    # def save(self, game: CurrentGame) -> None:
    #     pass

    # @abstractmethod
    # def get(self, game_id) -> CurrentGame:
    #     pass
