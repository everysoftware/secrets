from domain.auth import TwoFALogin
from domain.user import UserScheme
from infrastructure import User
from infrastructure.auth import generate_uri
from infrastructure.auth.otp import validate_otp
from infrastructure.utils import generate_qr_code


class AuthService:
    @staticmethod
    def generate_otp_qr_code(user: UserScheme) -> str:
        return generate_qr_code(generate_uri(user.otp_secret, user.email))

    @staticmethod
    def check_otp(user: UserScheme, login: TwoFALogin) -> bool:
        return validate_otp(login.one_time_password, user.otp_secret)
