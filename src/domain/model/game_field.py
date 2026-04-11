from constants import SIZE_FIELD


class GameField():
    def __init__(self):
        self.field = [[' ' for _ in range(SIZE_FIELD)] for _ in range(SIZE_FIELD)]
