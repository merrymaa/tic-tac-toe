from domain.model.game import CurrentGame
from datasource.database.database import Games
from web.model.game_web import GameWebDTO


class Mapper:
    """"
    WebDTO
    DomainDTO
    DatasourceDTO

    Преобразует модели DTO между собой
    """

    @staticmethod
    def datasource_to_domain(datasource_dto: Games) -> CurrentGame:
        game_domain = CurrentGame()
        game_domain.date_created = datasource_dto.date_created
        game_domain.uuid = datasource_dto.uuid
        game_domain.field.field = datasource_dto.field
        game_domain.status = datasource_dto.status  # waiting, game
        game_domain.type = datasource_dto.type
        game_domain.step_player = datasource_dto.step_player  # следующий ход игрока
        game_domain.player_1_uuid = datasource_dto.player_1_uuid  # UUID игрока за X
        game_domain.player_2_uuid = datasource_dto.player_2_uuid  # UUID игрока за O (для компьютера = "computer")
        game_domain.player_1_sign = datasource_dto.player_1_sign
        game_domain.player_2_sign = datasource_dto.player_2_sign
        game_domain.draw = datasource_dto.draw  # ничья
        game_domain.winner = datasource_dto.winner

        return game_domain

    @staticmethod
    def domain_to_datasource(game: CurrentGame) -> Games:
        """DomainDTO to DatasourceDTO"""

        datasource_dto = Games()
        datasource_dto.uuid = game.uuid
        datasource_dto.date_created = game.date_created
        datasource_dto.field = game.field.field
        datasource_dto.status = game.status  # waiting, game
        datasource_dto.type = game.type
        datasource_dto.step_player = game.step_player  # следующий ход игрока
        datasource_dto.player_1_uuid = game.player_1_uuid  # UUID игрока за X
        datasource_dto.player_2_uuid = game.player_2_uuid  # UUID игрока за O (для компьютера = "computer")
        datasource_dto.player_1_sign = game.player_1_sign
        datasource_dto.player_2_sign = game.player_2_sign
        datasource_dto.draw = game.draw  # ничья
        datasource_dto.winner = game.winner

        return datasource_dto

    @staticmethod
    def datasource_to_web(game_datasource: Games) -> GameWebDTO:
        game_web = GameWebDTO(uuid=game_datasource.uuid)

        game_web.date_created = game_datasource.date_created
        game_web.field.field = game_datasource.field.field
        game_web.status = game_datasource.status  # waiting, game
        game_web.type = game_datasource.type
        game_web.step_player = game_datasource.step_player  # следующий ход игрока
        game_web.player_1_uuid = game_datasource.player_1_uuid  # UUID игрока за X
        game_web.player_2_uuid = game_datasource.player_2_uuid  # UUID игрока за O (для компьютера = "computer")
        game_web.player_1_sign = game_datasource.player_1_sign
        game_web.player_2_sign = game_datasource.player_2_sign
        game_web.draw = game_datasource.draw  # ничья
        game_web.winner = game_datasource.winner

        return game_web
