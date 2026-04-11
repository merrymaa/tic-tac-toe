from datasource.repository.repository_backed_service import RepositoryBackedService
from web.model.game_web import GameWebDTO
from domain.model.game import CurrentGame
from web.mapper.web_mapper import WebMapper
from web.model.field_web import FieldWeb


class ControllerWeb():

    def __init__(self, game_service: RepositoryBackedService):
        self.game_service = game_service

    def make_move(self, game_web: GameWebDTO) -> GameWebDTO:
        domain_game = WebMapper.to_domain(game_web)
        updated_game = self.game_service.get_next_step(domain_game)
        game_web_result = WebMapper.to_web(updated_game)

        if isinstance(game_web_result.field, list):
            field_obj = FieldWeb()
            field_obj.field = game_web_result.field
            game_web_result.field = field_obj

        return game_web_result
