from abc import ABC, abstractmethod
from datasource.database.database import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def register_user(self, login: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def get_user(self, user_uuid) -> User:
        pass