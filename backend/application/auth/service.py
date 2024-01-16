from domain.user import BaseUserRepository
from domain.user.schemes import TwoFALogin, UserRead
from infrastructure import User
from infrastructure.auth import generate_uri
from infrastructure.auth.otp import validate_otp
from infrastructure.utils import generate_qr_code


class AuthService:
    def __init__(self, repository: BaseUserRepository):
        self.repository = repository

    @staticmethod
    def generate_otp_qr_code(user: User) -> str:
        return generate_qr_code(generate_uri(user.secret_otp, user.email))

    @staticmethod
    def check_otp(user: User, login: TwoFALogin) -> bool:
        return validate_otp(login.otp, user.secret_otp)

    def enable_two_fa(self, user: User) -> None:
        self.repository.enable_two_fa(UserRead.model_validate(user))
