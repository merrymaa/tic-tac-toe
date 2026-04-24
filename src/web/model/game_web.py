from web.model.field_web import FieldWeb
from uuid import uuid4


class GameWebDTO:
    def __init__(self, uuid=None, field=None):
        self.uuid = str(uuid4()) if not uuid else uuid
        self.field = FieldWeb() if not field else field
        self.status = None  # waiting, game
        self.type = None
        self.step_player = None  # следующий ход игрока
        self.player_1_uuid = None  # UUID игрока за X
        self.player_2_uuid = None  # UUID игрока за O (для компьютера = "computer")
        self.player_1_sign = None
        self.player_2_sign = None
        self.draw = None  # ничья
        self.winner = None

    def set_uuid_player(self, uuid: str):
        self.player_1_uuid = uuid

    def set_game_type(self, game_type: str):
        if game_type == "AI":
            self.type = game_type
            self.player_2_uuid = "computer"
            self.step_player = self.player_1_uuid

        if game_type == "HUMAN":
            self.type = game_type
            self.step_player = self.player_1_uuid
