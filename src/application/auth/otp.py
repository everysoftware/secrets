from pyotp import random_base32, totp

from src.infrastructure.config import settings


def generate_secret() -> str:
    return random_base32()


def generate_uri(secret: str, email: str) -> str:
    otp = totp.TOTP(secret)
    uri = otp.provisioning_uri(name=email, issuer_name=settings.app.product)

    return uri


def validate_otp(otp: str, secret: str) -> bool:
    return totp.TOTP(secret).verify(otp)
