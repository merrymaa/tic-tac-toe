from constants import SIZE_FIELD
from typing import List


class FieldDTO():
    def __init__(self):
        self.field: List[List[str]] = [[' ' for _ in range(SIZE_FIELD)] for _ in range(SIZE_FIELD)]
