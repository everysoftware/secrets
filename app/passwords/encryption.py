from typing import Any

from app.config import settings
from app.security.encryption import encrypt_aes, decrypt_aes


def encrypt_password(data: dict[str, Any]) -> dict[str, Any]:
    password = data.pop("password", None)  # type: str | None
    if password is not None:
        data["encrypted_password"] = encrypt_aes(
            password, settings.app.encryption_secret
        )
    username = data.pop("username", None)  # type: str | None
    if username is not None:
        data["encrypted_username"] = encrypt_aes(
            username, settings.app.encryption_secret
        )
    return data


def decrypt_password(data: dict[str, Any]) -> dict[str, Any]:
    password = data.pop("encrypted_password", None)  # type: str | None
    if password is not None:
        data["password"] = decrypt_aes(
            password, settings.app.encryption_secret
        )
    username = data.pop("encrypted_username", None)  # type: str | None
    if username is not None:
        data["username"] = decrypt_aes(
            username, settings.app.encryption_secret
        )
    return data
