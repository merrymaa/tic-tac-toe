from web.model import game_web
from web.model.game_web import GameWebDTO
from domain.model.game import CurrentGame
from datasource.database.database import Games


class WebMapper:
    """"
    Преобразует объекты между собой:
    game_web - объект web слоя
    game_bd - объект БД
    game_domain- объект домаин слоя
    """

    @staticmethod
    def to_web(game: CurrentGame) -> GameWebDTO:
        """"Преобразование объекта домаин слоя Game в объект веб слоя GameWebDTO"""
        game_web_dto = GameWebDTO(game.UUID, game.field.field)

        return game_web_dto

    @staticmethod
    def to_domain(game_web_dto: GameWebDTO) -> CurrentGame:
        """"Преобразование объекта веб слоя GameWebDTO в объект домаин слоя Game"""
        game = CurrentGame()
        game.UUID = game_web_dto.uuid
        game.field.field = game_web_dto.field.field

        return game

    @staticmethod
    def from_web_to_db(game_web: GameWebDTO) -> Games:
        game_db = Games(uuid=game_web.uuid, field=game_web.field.field, player_1_uuid=game_web.player_uuid, type=game_web.game_type,
                        step_player=game_web.step_next_player, player_2_uuid=game_web.player_2)

        return game_db
