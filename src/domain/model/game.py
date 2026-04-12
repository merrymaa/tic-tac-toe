import uuid
from domain.model.game_field import GameField
from datasource.model.user import User


class CurrentGame():

    def __init__(self):
        self.field = GameField()
        self.UUID = uuid.uuid4()
        self.user_info = User()

    def set_user_name(self, user_name):
        self.user_info.name = user_name
