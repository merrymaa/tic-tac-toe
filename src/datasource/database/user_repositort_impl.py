from datasource.database.database import User, SessionLocal
from datasource.database.user_repository_interface import UserRepository
from datasource.database.sign_up_request import SignUpRequest
from uuid import uuid4


class UserRepositoryImpl(UserRepository):

    def __init__(self):
        self.session_db = SessionLocal()


    def save(self, user: User):
        new_user = User(uuid=user.uuid, login=user.login, hashed_password=user.hashed_password)
        self.session_db.add(new_user)
        self.session_db.commit()
        self.session_db.close()

    def register_user(self, sign_up_request: SignUpRequest):
        user_login = sign_up_request.body.login
        user_password = sign_up_request.body.password
        user_uuid = str(uuid4())
        new_user = User(uuid=user_uuid, login=user_login, hashed_password=user_password)

        try:
            existing_user = self.session_db.query(User).filter(User.login == new_user.login).first()
            if existing_user is not None:
                raise ValueError(f"Пользователь с логином {new_user.login} уже существует")

            self.session_db.add(new_user)
            self.session_db.commit()
            print(f"Пользователь с логином {new_user.login} добавлен в БД")
        except Exception as e:
            self.session_db.rollback()
            print(f"Ошибка при сохранении пользователя в БД: {e}")
            raise
        finally:
            self.session_db.close()

    def get_by_login(self, login: str) -> User:
        pass
