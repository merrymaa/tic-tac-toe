from datasource.repository.repository_backed_service import RepositoryBackedService
from web.model.game_web import GameWebDTO
from domain.model.game import CurrentGame
from web.mapper.web_mapper import WebMapper
from web.model.field_web import FieldWeb


class ControllerWeb:

    def __init__(self, game_service: RepositoryBackedService):
        self.game_service = game_service

    def make_move(self, game_web: GameWebDTO) -> GameWebDTO:

        domain_game = WebMapper.web_to_domain(game_web)
        if game_web.type == "AI":
            updated_game = self.game_service.get_next_step(domain_game) # объект domain слоя CurrentGame
            game_web_result = WebMapper.domain_to_web(updated_game)
        else:
            print("=======Step done")
            updated_game = self.game_service.make_step(domain_game)
            # self.game_service.save_game(domain_game)
            game_web_result = WebMapper.domain_to_web(updated_game)
        return game_web_result

    def download_game(self, game_uuid) -> GameWebDTO:

        downloaded_game = self.game_service.get_game(game_uuid)
        return WebMapper.domain_to_web(downloaded_game)

    def join_game(self, player_uuid: str) -> GameWebDTO:
        joined_game = self.game_service.join_game(player_uuid)
        return WebMapper.domain_to_web(joined_game)
