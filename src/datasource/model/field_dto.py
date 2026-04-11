from constants import SIZE_FIELD


class FieldDTO():
    def __init__(self):
        self.field = [[0 for _ in range(SIZE_FIELD)] for _ in range(SIZE_FIELD)]
