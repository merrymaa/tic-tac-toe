from datasource.database.database import User, SessionLocal
from datasource.repository.user_repository_interface import UserRepository
from uuid import uuid4


class UserRepositoryImpl(UserRepository):

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def save(self, user: User):
        session_db = self.session_factory()
        new_user = User(uuid=user.uuid, login=user.login, hashed_password=user.hashed_password)
        session_db.add(new_user)
        session_db.commit()
        session_db.close()

    def register_user(self, login: str, hashed_password: str) -> bool:
        """"Регистрация нового пользователя в БД"""
        session_db = self.session_factory()
        new_user = User(uuid=str(uuid4()), login=login, hashed_password=hashed_password)
        try:
            existing_user = session_db.query(User).filter(User.login == new_user.login).first()
            if existing_user:
                print(f"Пользователь с логином {new_user.login} уже существует")
                return False
            session_db.add(new_user)
            session_db.commit()
            print(f"Пользователь с логином {new_user.login} добавлен в БД")
            return True
        except Exception as e:
            session_db.rollback()
            print(f"Ошибка при сохранении пользователя в БД: {e}")
            raise
        finally:
            session_db.close()

    def find_by_login(self, login: str) -> User:
        """"Ищет пользователя по логину и возвращает его UUID (str)"""
        session_db = self.session_factory()
        try:
            return session_db.query(User).filter(User.login == login).first()

        finally:
            session_db.close()

    def get_user(self, user_uuid) -> User:
        with self.session_factory() as session:
            current_user = session.query(User).filter(User.uuid == user_uuid).first()
            return current_user
