from src.infrastructure.config import settings
from src.domain.schemes import (
    SPasswordCreate,
    SPasswordCreateEncrypted,
    SPasswordEncrypted,
    SPassword,
    SPasswordUpdate,
    SPasswordUpdateEncrypted,
    SPasswordGenerate,
)
from src.application.security import encrypt_aes, decrypt_aes, generate_password
from .base import Service


class SecurityService(Service):
    @staticmethod
    def encrypt_password_create(scheme: SPasswordCreate) -> SPasswordCreateEncrypted:
        """Encrypt create scheme."""
        return SPasswordCreateEncrypted(
            **scheme.model_dump(exclude={"username", "password"}),
            username=encrypt_aes(scheme.username, settings.app.encryption_secret),
            password=encrypt_aes(scheme.password, settings.app.encryption_secret),
        )

    @staticmethod
    def decrypt_password(scheme: SPasswordEncrypted) -> SPassword:
        """Decrypt password scheme."""
        return SPassword(
            **scheme.model_dump(exclude={"username", "password"}),
            username=decrypt_aes(scheme.username, settings.app.encryption_secret),
            password=decrypt_aes(scheme.password, settings.app.encryption_secret),
        )

    @staticmethod
    def encrypt_password_update(scheme: SPasswordUpdate) -> SPasswordUpdateEncrypted:
        """Encrypt update scheme."""
        scheme_dump = scheme.model_dump(
            exclude_unset=True, exclude={"username", "password"}
        )

        if scheme.username is not None:
            scheme_dump["username"] = encrypt_aes(
                scheme.username, settings.app.encryption_secret
            )

        if scheme.password is not None:
            scheme_dump["password"] = encrypt_aes(
                scheme.password, settings.app.encryption_secret
            )

        return SPasswordUpdateEncrypted(**scheme_dump)

    @staticmethod
    async def generate(password_settings: SPasswordGenerate) -> str:
        """Generate a new password."""
        return generate_password(password_settings)
