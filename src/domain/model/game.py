from uuid import uuid4
from domain.model.game_field import GameField


class CurrentGame:

    def __init__(self, uuid=None):
        self.field = GameField()
        self.uuid = str(uuid4()) if not uuid else uuid
        self.status = None
        self.type = None
        self.step_player = None
        self.player_1_uuid = None  # UUID игрока за X
        self.player_2_uuid = None  # UUID игрока за O (для компьютера = "computer")
        self.player_1_sign = 'X'
        self.player_2_sign = 'O'
        self.draw = None  # ничья
        self.winner = None

    def _get_winner(self) -> str | None:
        field = self.field.field
        for row in field:
            if row[0] == row[1] == row[2] == self.player_1_sign:
                return self.player_1_uuid
            if row[0] == row[1] == row[2] == self.player_2_sign:
                return self.player_2_uuid
        for n in range(3):
            if field[0][n] == field[1][n] == field[2][n] == self.player_1_sign:
                return self.player_1_uuid
            if field[0][n] == field[1][n] == field[2][n] == self.player_2_sign:
                return self.player_2_uuid
        if field[0][0] == field[1][1] == field[2][2] == self.player_1_sign or field[0][2] == field[1][1] == field[2][
            0] == self.player_1_sign:
            return self.player_1_uuid
        if field[0][0] == field[1][1] == field[2][2] == self.player_2_sign or field[0][2] == field[1][1] == field[2][
            0] == self.player_2_sign:
            return self.player_2_uuid
        return None

    def set_game_over(self) -> None:
        if not self._get_winner():
            self.draw = True
        else:
            self.winner = self._get_winner()
            self.draw = False
