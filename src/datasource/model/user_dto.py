class UserDTO():
    """"Объект для передачи данных между domain и БД"""

    def __init__(self):
        self.name = ""
        self.password_hash: str = ""
