import uuid
from domain.model.game_field import GameField


class CurrentGame():

    def __init__(self):
        self.field = GameField()
        self.UUID = uuid.uuid4()
