from datasource.mapper.mapper import Mapper
from domain.service.game_service import GameService
from datasource.repository.game_repository_impl import GameRepositoryImpl
from domain.service.game_service_imp import GameServiceMinimax
from domain.model.game import CurrentGame
from datasource.database.database import Games
from datasource.database.database import User


class RepositoryBackedService():

    def __init__(self):
        self.game_repository = GameRepositoryImpl()
        self.game_service = GameServiceMinimax()

    def create_game(self, player_uuid: str, game_type: str) -> CurrentGame | None:
        try:
            new_game = self.game_service.create_game(player_uuid, game_type)
            if not new_game:
                raise Exception
            self.game_repository.add_game(new_game)
            return new_game
        except Exception as e:
            print(f"Error in RepositoryBackedService.create_game: {e}")
            return None

    def make_step(self, game: CurrentGame, player_uuid: str) -> CurrentGame | None:
        """"Ход игры с человеком"""
        try:
            old_game = self.get_game(game.uuid)
            if self.validate_game(game, old_game) and self.game_service.check_step(game, player_uuid):
                if self.is_game_over(game):
                    game.status = "finish"
                    game.set_game_over()
                # сохранение после хода
                self.game_service.change_step(game, player_uuid)
                self.game_repository.save_game(game)
                return game
            else:
                print("===game not valid")
                return None
        except Exception as e:
            print(f"Step is not available: {e}")
            return None

    def get_next_step(self, game: CurrentGame) -> CurrentGame | None:
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
        return None

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

    def get_current_game(self, game_uuid: str) -> Games:
        return self.game_repository.get_current_game(game_uuid)

    def get_available_games(self, player_uuid: str) -> list[Games]:
        return self.game_repository.get_available_games(player_uuid)

    def get_finished_games(self, player_uuid: str) -> list[Games]:
        return self.game_repository.get_finished_games(player_uuid)

    def join_game(self, player_uuid: str) -> CurrentGame | None:
        try:
            game_for_join = self.get_available_games(player_uuid)
            if game_for_join:
                game = Mapper.datasource_to_domain(game_for_join[0])
                joined_game = self.game_service.join_game(player_uuid, game)
                self.save_game(joined_game)
                return joined_game
        except Exception as e:
            print(f"Player can't join to game: {e}")
            return None

    def get_user(self, user_uuid) -> User:
        return self.game_repository.get_user(user_uuid)

    def get_statistic(self, n: int) -> dict:
        return self.game_repository.get_statistic(n)
