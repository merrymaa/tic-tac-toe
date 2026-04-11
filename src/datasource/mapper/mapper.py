from domain.model.game import CurrentGame
from datasource.model.game_dto import GameDTO


class Mapper:
    """"
    Преобразует модель Game в DTO и обратно
    """

    @staticmethod
    def from_domain_to_storage(game: CurrentGame) -> GameDTO:
        game_dto = GameDTO()

        game_dto.field.field = game.field.field
        game_dto.uuid = game.UUID

        return game_dto

    @staticmethod
    def from_storage_to_domain(game_dto: GameDTO) -> CurrentGame:
        game = CurrentGame()
        game.UUID = game_dto.uuid
        game.field.field = game_dto.field.field

        return game
