from abc import ABC, abstractmethod
from datasource.model.sign_up_request import SignUpRequest


class UserService(ABC):
    @abstractmethod
    def register(self, sign_up_request: SignUpRequest) -> bool:
        pass