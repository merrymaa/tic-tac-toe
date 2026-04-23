from datasource.repository.repository_backed_service import RepositoryBackedService
from web.model.game_web import GameWebDTO
from domain.model.game import CurrentGame
from web.mapper.web_mapper import WebMapper
from web.model.field_web import FieldWeb


class ControllerWeb:

    def __init__(self, game_service: RepositoryBackedService):
        self.game_service = game_service

    def make_move(self, game_web: GameWebDTO, player_uuid: str) -> GameWebDTO:
        try:
            domain_game = WebMapper.web_to_domain(game_web)
            if game_web.type == "AI":
                updated_game = self.game_service.get_next_step(domain_game) # объект domain слоя CurrentGame
                game_web_result = WebMapper.domain_to_web(updated_game)
            else:
                updated_game = self.game_service.make_step(domain_game, player_uuid)
                game_web_result = WebMapper.domain_to_web(updated_game)
            return game_web_result
        except Exception as e:
            print(f"Error in ControllerWeb.make_move - {e}")
            raise

    def download_game(self, game_uuid) -> GameWebDTO:
        try:
            downloaded_game = self.game_service.get_game(game_uuid)
            return WebMapper.domain_to_web(downloaded_game)
        except Exception as e:
            print(f"Error in ControllerWeb.download_game - {e}")
            raise

    def join_game(self, player_uuid: str) -> GameWebDTO | None:
        try:
            joined_game = self.game_service.join_game(player_uuid)
            if joined_game:
                return WebMapper.domain_to_web(joined_game)
            return None
        except Exception as e:
            print(f"Error in ControllerWeb.join_game - {e}")
            raise
