from abc import ABC, abstractmethod
from datasource.database.database import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    # @abstractmethod
    # def get_by_login(self, login: str) -> User:
    #     pass

    @abstractmethod
    def register_user(self, login: str, hashed_password: str) -> bool:
        pass