from web.model.game_web import GameWebDTO
from domain.model.game import CurrentGame


class WebMapper:
    """"Преобразует Game в GameWebDTO и обратно
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
