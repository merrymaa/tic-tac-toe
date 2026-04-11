from domain.service.game_service import GameService
from domain.model.game import CurrentGame
from constants import HUMAN, AI, BEST_SCORE_MAX, BEST_SCORE_MIN


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

    def validate_game(self, game: CurrentGame) -> bool:
        field = game.field.field

        count_human = sum(row.count(HUMAN) for row in field)
        count_ai = sum(row.count(AI) for row in field)

        if not (count_human == count_ai or count_human == count_ai + 1):
            return False

        human_win = self.check_win(field, HUMAN)
        ai_win = self.check_win(field, AI)
        if human_win and ai_win:
            return False

        if human_win and count_human != count_ai + 1:
            return False
        if ai_win and count_human != count_ai:
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
