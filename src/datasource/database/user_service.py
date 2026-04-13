from abc import ABC, abstractmethod
from datasource.database.database import User


class UserService(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    def get_by_login(self, login: str) -> User:
        pass
