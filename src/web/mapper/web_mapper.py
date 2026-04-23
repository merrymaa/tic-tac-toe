from web.model.game_web import GameWebDTO
from domain.model.game import CurrentGame


class WebMapper:
    """"
    WebDTO
    DomainDTO
    DatasourceDTO

    Преобразует объекты между собой

    """
    @staticmethod
    def datasource_to_web(datasource_dto) -> GameWebDTO:
        try:
            game_web = GameWebDTO()

            game_web.uuid = datasource_dto.uuid
            game_web.field.field = datasource_dto.field
            game_web.status = datasource_dto.status  # waiting, game
            game_web.type = datasource_dto.type
            game_web.step_player = datasource_dto.step_player  # следующий ход игрока
            game_web.player_1_uuid = datasource_dto.player_1_uuid  # UUID игрока за X
            game_web.player_2_uuid = datasource_dto.player_2_uuid  # UUID игрока за O (для компьютера = "computer")
            game_web.player_1_sign = datasource_dto.player_1_sign
            game_web.player_2_sign = datasource_dto.player_2_sign
            game_web.draw = datasource_dto.draw  # ничья
            game_web.winner = datasource_dto.winner

            return game_web
        except Exception as e:
            print(f"Error in datasource_to_web - {e}")
            raise

    # web_to_domain
    @staticmethod
    def web_to_domain(game_web: GameWebDTO) -> CurrentGame:
        try:
            game_domain = CurrentGame()

            game_domain.uuid = game_web.uuid
            game_domain.field.field = game_web.field.field
            game_domain.status = game_web.status  # waiting, game
            game_domain.type = game_web.type
            game_domain.step_player = game_web.step_player  # следующий ход игрока
            game_domain.player_1_uuid = game_web.player_1_uuid  # UUID игрока за X
            game_domain.player_2_uuid = game_web.player_2_uuid  # UUID игрока за O (для компьютера = "computer")
            game_domain.player_1_sign = game_web.player_1_sign
            game_domain.player_2_sign = game_web.player_2_sign
            game_domain.draw = game_web.draw  # ничья
            game_domain.winner = game_web.winner

            return game_domain
        except Exception as e:
            print(f"Error in web_to_domain - {e}")
            raise


    @staticmethod
    def domain_to_web(game_domain: CurrentGame ) -> GameWebDTO:
        try:
            game_web = GameWebDTO()

            game_web.uuid = game_domain.uuid
            game_web.field.field = game_domain.field.field
            game_web.status = game_domain.status
            game_web.type = game_domain.type
            game_web.step_player = game_domain.step_player  # следующий ход игрока
            game_web.player_1_uuid = game_domain.player_1_uuid  # UUID игрока за X
            game_web.player_2_uuid = game_domain.player_2_uuid  # UUID игрока за O (для компьютера = "computer")
            game_web.player_1_sign = game_domain.player_1_sign
            game_web.player_2_sign = game_domain.player_2_sign
            game_web.draw = game_domain.draw  # ничья
            game_web.winner = game_domain.winner
            return game_web
        except Exception as e:
            print(f"Error in domain_to_web - {e}")
            raise

    # @staticmethod
    # def to_web(game: CurrentGame) -> GameWebDTO:
    #     """"Преобразование объекта домаин слоя Game в объект веб слоя GameWebDTO"""
    #     game_web_dto = GameWebDTO(game.uuid, game.field.field)
    #
    #     return game_web_dto
    #
    # @staticmethod
    # def to_domain(game_web_dto: GameWebDTO) -> CurrentGame:
    #     """"Преобразование объекта веб слоя GameWebDTO в объект домаин слоя Game"""
    #     game = CurrentGame()
    #     game.UUID = game_web_dto.uuid
    #     game.field.field = game_web_dto.field.field
    #
    #     return game
    #
    # @staticmethod
    # def from_web_to_db(game_web: GameWebDTO) -> Games:
    #     game_db = Games(uuid=game_web.uuid, field=game_web.field.field, player_1_uuid=game_web.player_uuid,
    #                     type=game_web.game_type,
    #                     step_player=game_web.step_next_player, player_2_uuid=game_web.player_2)
    #
    #     return game_db
