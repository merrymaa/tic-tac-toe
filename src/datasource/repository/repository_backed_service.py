from datasource.mapper.mapper import Mapper
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

    def make_step(self, game: CurrentGame) -> CurrentGame:
        """"Ход игры с человеком"""
        old_game = self.get_game(game.uuid)
        if self.validate_game(game, old_game):
            print("====Game is valid")
            if self.is_game_over(game):
                game.status = "finish"
                game.set_game_over()

            self.game_repository.save_game(game)

        return game

        pass
    def get_next_step(self, game: CurrentGame) -> CurrentGame:
        """"Ход игры с компьютером"""
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

    def get_active_games(self) -> list[Games]:
        return self.game_repository.get_active_games()

    def get_game(self, game_uuid: str) -> CurrentGame:
        return self.game_repository.get_game(game_uuid)

    def get_available_games(self, player_uuid: str) -> list[Games]:
        return self.game_repository.get_available_games(player_uuid)

    def join_game(self, player_uuid: str) -> CurrentGame:

        game_for_join = self.get_available_games(player_uuid)
        game = Mapper.datasource_to_domain(game_for_join[1])
        joined_game = self.game_service.join_game(player_uuid, game)
        self.save_game(joined_game)

        return joined_game
