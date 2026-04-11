from abc import ABC, abstractmethod
from domain.model.game import CurrentGame


class Repository(ABC):
    """
    Интерфейс репозитория.
    Сохраняет игру в хранилище и получает игру по uuid из хранилища.
    """

    @abstractmethod
    def save(self, game: CurrentGame) -> None:
        pass

    @abstractmethod
    def get(self, game_id) -> CurrentGame:
        pass
