from datasource.service.user_service import UserService
from datasource.model.sign_up_request import SignUpRequest
from werkzeug.security import generate_password_hash, check_password_hash
from datasource.repository.user_repository_impl import UserRepositoryImpl


class UserServiceImpl(UserService):
    def __init__(self):
        self.user_rep = UserRepositoryImpl()

    def register(self, sign_up_request: SignUpRequest) -> bool:
        hashed_password = generate_password_hash(sign_up_request.password)

        return self.user_rep.register_user(sign_up_request.login, hashed_password)

    def authorize(self, login: str, password: str) -> str | None:
        user = self.user_rep.find_by_login(login)
        if user and check_password_hash(user.hashed_password, password):
            print("Authorization is successful")
            return user.uuid

        return None
