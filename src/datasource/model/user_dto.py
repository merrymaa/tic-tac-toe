class UserDTO():
    """"Объект для передачи данных между domain и БД"""

    def __init__(self):
        self.uuid: str = None
        self.login = ""
        self.password_hash: str = ""
