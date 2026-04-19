from web.model.field_web import FieldWeb
from uuid import uuid4


class GameWebDTO:
    def __init__(self):
        self.uuid = str(uuid4())
        self.field = FieldWeb()
        self.game_type = None
        self.player_uuid = None
        self.player_2 = None
        self.step_next_player = None

    def set_uuid_player(self, uuid: str):
        self.player_uuid = uuid

    def set_game_type(self, game_type: str):
        if game_type == "AI":
            self.game_type = game_type
            self.player_2 = "computer"
            self.step_next_player = self.player_uuid

        if game_type == "HUMAN":
            self.game_type = game_type
            self.step_next_player = self.player_uuid
