from uuid import uuid4


class User:
    def __init__(self, login: str, password: str):
        self.uuid = str(uuid4())
        self.login = login
        self.hashed_password: str = password