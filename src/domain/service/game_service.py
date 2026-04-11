from abc import ABC, abstractmethod
from domain.model.game import CurrentGame


class GameService(ABC):
    @abstractmethod
    def get_next_step(self, game: CurrentGame) -> CurrentGame:
        pass

    @abstractmethod
    def validate_game(self, game: CurrentGame) -> bool:
        pass

    @abstractmethod
    def is_game_over(self, game: CurrentGame) -> bool:
        pass
