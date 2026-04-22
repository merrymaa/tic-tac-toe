from domain.service.game_service import GameService
from datasource.repository.game_repository_impl import GameRepositoryImpl
from datasource.repository.user_repository_impl import UserRepositoryImpl
from domain.service.game_service_imp import GameServiceMinimax
from domain.model.game import CurrentGame
from datasource.database.database import Games
from datasource.database.database import User
from web.model.game_web import GameWebDTO


class RepositoryBackedService(GameService):

    def __init__(self):
        self.game_repository = GameRepositoryImpl()
        self.game_service = GameServiceMinimax()


    def get_next_step(self, game: CurrentGame) -> CurrentGame:
        old_game = self.get_game(game.uuid)
        if self.validate_game(game, old_game):
            if game.status == "waiting":
                game.status = "active"
            if self.is_game_over(game):
                game.status = "finish"
                game.set_game_over()
                self.game_repository.save_game(game)

            else:
                self.game_service.get_next_step(game)
                if self.is_game_over(game):
                    game.status = "finish"
                    game.set_game_over()
                self.game_repository.save_game(game)

        return game

    def save_game(self, game: CurrentGame):
        self.game_repository.save_game(game)

    def add_game(self, game: CurrentGame):
        self.game_repository.save_game(game)

    def validate_game(self, current_game: CurrentGame, old_game: CurrentGame) -> bool:

        return self.game_service.validate_game(current_game, old_game)

    def is_game_over(self, game: CurrentGame) -> bool:
        return self.game_service.is_game_over(game)

    def get_active_games(self) -> list:
        return self.game_repository.get_active_games()

    def get_game(self, game_uuid: str) -> CurrentGame:
        return self.game_repository.get_game(game_uuid)
