from abc import ABC, abstractmethod
from datasource.database.sign_up_request import SignUpRequest
from datasource.database.database import User



class UserService(ABC):
    @abstractmethod
    def register(self, sign_up_request: SignUpRequest) -> bool:
        pass