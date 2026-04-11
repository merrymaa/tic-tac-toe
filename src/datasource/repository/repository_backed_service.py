from domain.service.game_service import GameService
from datasource.repository.repository_impl import GameRepository
from domain.service.game_service_imp import GameServiceMinimax
from domain.model.game import CurrentGame


class RepositoryBackedService(GameService):

    def __init__(self, repository: GameRepository):
        self.repository = repository
        self.game_service = GameServiceMinimax()

    def get_next_step(self, game: CurrentGame) -> CurrentGame:
        self.game_service.get_next_step(game)
        print("========================Ход сделан, Игра сохранена")
        self.repository.save(game)
        return game

    def validate_game(self, game: CurrentGame) -> bool:
        return self.game_service.validate_game(game)

    def is_game_over(self, game: CurrentGame) -> bool:
        return self.game_service.is_game_over(game)
