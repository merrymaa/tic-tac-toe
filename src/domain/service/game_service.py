from abc import ABC, abstractmethod
from domain.model.game import CurrentGame


class GameService(ABC):
    @abstractmethod
    def get_next_step(self, game: CurrentGame) -> CurrentGame:
        pass

    @abstractmethod
    def validate_game(self, current_game: CurrentGame, old_game: CurrentGame) -> bool:
        pass

    @abstractmethod
    def is_game_over(self, game: CurrentGame) -> bool:
        pass

    @abstractmethod
    def join_game(self, player_uuid: str, game: CurrentGame) -> CurrentGame:
        pass

    @abstractmethod
    def create_game(self, player_uuid: str, game_type: str) -> CurrentGame | None:
        pass

    @abstractmethod
    def check_win(self, field, player) -> bool:
        pass

    @abstractmethod
    def check_step(self, game: CurrentGame, player_uuid: str) -> bool:
        pass

    @abstractmethod
    def change_step(self, game: CurrentGame, player_uuid: str) -> None:
        pass
