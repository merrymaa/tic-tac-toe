from datasource.database.database import User, SessionLocal
from datasource.database.user_service import UserService


class UserServiceImpl(UserService):

    def __init__(self, session):
        self.session_db: SessionLocal = session
    def save(self, user: User):

        new_user = User(uuid=user.uuid, login=user.login, hashed_password=user.hashed_password)
        self.session_db.add(new_user)
        self.session_db.commit()
        self.session_db.close()

    def get_by_login(self, login: str) -> User:
        pass
