from domain.schemes import UserScheme
from domain.schemes.dtos import TwoFALogin
from infrastructure.utils import generate_qr_code, validate_otp, generate_uri
from .base import Service


class AuthService(Service):
    @staticmethod
    def generate_otp_qr_code(user: UserScheme) -> str:
        return generate_qr_code(generate_uri(user.otp_secret, user.email))

    @staticmethod
    def check_otp(user: UserScheme, login: TwoFALogin) -> bool:
        return validate_otp(login.one_time_password, user.otp_secret)
