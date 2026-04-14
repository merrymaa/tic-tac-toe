from domain.service.user_service import UserService
from datasource.database.sign_up_request import SignUpRequest
from werkzeug.security import generate_password_hash
from datasource.database.user_repositort_impl import UserRepositoryImpl


class UserServiceImpl(UserService):
    def __init__(self, user_rep: UserRepositoryImpl):
        self.user_rep = user_rep

    def register(self, sign_up_request: SignUpRequest) -> bool:
        hashed_password = generate_password_hash(sign_up_request.password)

        return self.user_rep.register_user(sign_up_request.login, hashed_password)




