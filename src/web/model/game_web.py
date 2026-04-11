from web.model.field_web import FieldWeb
from uuid import UUID


class GameWebDTO():
    def __init__(self, game_uuid: UUID, field: FieldWeb):
        self.uuid = game_uuid
        self.field = field


