from domain.service.game_service import GameService
from domain.model.game import CurrentGame
from constants import HUMAN, AI, BEST_SCORE_MAX, BEST_SCORE_MIN, SIZE_FIELD


class GameServiceMinimax(GameService):
    """
    Реализация сервиса игры с алгоритмом Минимакс
    """

    def get_next_step(self, game: CurrentGame) -> CurrentGame:
        # if self.validate_game(game):
        field = game.field.field
        best_score = -100
        best_step = None

        for step in self._available_steps(field):
            field[step[0]][step[1]] = AI
            score = self._minimax(field, 0, False)
            field[step[0]][step[1]] = ' '

            if score > best_score:
                best_score = score
                best_step = step

        if best_step:
            game.field.field[best_step[0]][best_step[1]] = AI

        return game

    @staticmethod
    def _available_steps(field) -> list:
        steps = []
        for i in range(3):
            for j in range(3):
                if field[i][j] not in [HUMAN, AI]:
                    steps.append((i, j))
        return steps

    def _minimax(self, field, depth, is_max):
        if self.check_win(field, AI):
            return 10 - depth
        if self.check_win(field, HUMAN):
            return -10 + depth
        if not self._available_steps(field):
            return 0

        if is_max:
            best_score = BEST_SCORE_MIN
            for step in self._available_steps(field):
                field[step[0]][step[1]] = AI
                score = self._minimax(field, depth + 1, False)
                field[step[0]][step[1]] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = BEST_SCORE_MAX
            for step in self._available_steps(field):
                field[step[0]][step[1]] = HUMAN
                score = self._minimax(field, depth + 1, True)
                field[step[0]][step[1]] = ' '
                best_score = min(score, best_score)
            return best_score

    def validate_game(self, current_game: CurrentGame, old_game: CurrentGame) -> bool:
        """Функция проверяет неизменность предыдущих ходов"""
        if current_game.status == "finish":
            return False
        current_field = current_game.field.field
        old_field = old_game.field.field

        for i in range(SIZE_FIELD):
            for j in range(SIZE_FIELD):
                if old_field[i][j] == HUMAN or old_field[i][j] == AI:
                    if current_field[i][j] != old_field[i][j]:
                        return False
        changes = 0 # количество изменений
        sign = None # Знак которым осуществлен ход
        for i in range(SIZE_FIELD):
            for j in range(SIZE_FIELD):
                if current_field[i][j] != old_field[i][j]:
                    changes += 1
                    sign = current_field[i][j]
        print(f"=== sign = {sign}")
        if old_game.step_player == old_game.player_1_uuid:
            print(f"===sign player: {old_game.player_1_sign} - {sign}")
            if old_game.player_1_sign != sign:
                return False
        if old_game.step_player == old_game.player_2_uuid:
            print(f"===sign player: {old_game.player_2_sign} - {sign}")
            if old_game.player_2_sign != sign:
                return False
        print(f"==chamges = {changes}")
        if changes != 1:
            return False
        return True




    @staticmethod
    def check_win(field, player) -> bool:
        for row in field:
            if row[0] == row[1] == row[2] == player:
                return True
        for n in range(3):
            if field[0][n] == field[1][n] == field[2][n] == player:
                return True
        if field[0][0] == field[1][1] == field[2][2] == player or field[0][2] == field[1][1] == field[2][0] == player:
            return True
        return False

    def is_game_over(self, game: CurrentGame) -> bool:
        return self.check_win(game.field.field, HUMAN) or self.check_win(game.field.field, AI)

    @staticmethod
    def join_game(player_uuid: str, game: CurrentGame) -> CurrentGame:

        game.player_2_uuid = player_uuid
        game.status = "active"

        return game
    @staticmethod
    def check_step(game: CurrentGame, player_uuid: str) -> bool:
        return game.step_player == player_uuid

        # # ход игрока 1
        # if game.step_player == game.player_1_uuid == player_uuid:
        #     game.step_player = game.player_2_uuid
        #     return True
        #
        # # ход игрока 2
        # if game.step_player == game.player_2_uuid == player_uuid:
        #     game.step_player = game.player_1_uuid
        #     return True
        # print(f"=== нарушен порядок хода")
        # return False

    @staticmethod
    def change_step(game: CurrentGame, player_uuid: str) -> None:
        # ход игрока 1
        if game.step_player == game.player_1_uuid == player_uuid:
            game.step_player = game.player_2_uuid
            print("===== 1 -> 2")

        # ход игрока 2
        if game.step_player == game.player_2_uuid == player_uuid:
            game.step_player = game.player_1_uuid
            print("===== 2 -> 1")

    @staticmethod
    def create_game(player_uuid: str, game_type: str) -> CurrentGame | None:
        try:
            if game_type != "HUMAN" and game_type != "AI":
                raise ValueError

            new_game = CurrentGame()
            new_game.player_1_uuid = player_uuid
            new_game.step_player = player_uuid
            new_game.status = "waiting"
            new_game.type = game_type
            if game_type == "AI":
                new_game.player_2_uuid = "computer"

            return new_game
        except Exception as e:
            print(f"Error in game_type: {e}")