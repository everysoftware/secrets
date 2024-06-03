from secrets_app.passwords.schemas import (
    SPasswordCreate,
    SPasswordCreateEncrypted,
    SPasswordEncrypted,
    SPassword,
    SPasswordUpdate,
    SPasswordUpdateEncrypted,
)
from secrets_app.security.encryption import encrypt_aes, decrypt_aes
from secrets_app.settings import settings


class PasswordEncryption:
    @staticmethod
    def encrypt_password_create(scheme: SPasswordCreate) -> SPasswordCreateEncrypted:
        return SPasswordCreateEncrypted(
            **scheme.model_dump(exclude={"username", "password"}),
            username=encrypt_aes(scheme.username, settings.app.encryption_secret),
            password=encrypt_aes(scheme.password, settings.app.encryption_secret),
        )

    @staticmethod
    def decrypt_password(scheme: SPasswordEncrypted) -> SPassword:
        return SPassword(
            **scheme.model_dump(exclude={"username", "password"}),
            username=decrypt_aes(scheme.username, settings.app.encryption_secret),
            password=decrypt_aes(scheme.password, settings.app.encryption_secret),
        )

    @staticmethod
    def encrypt_password_update(scheme: SPasswordUpdate) -> SPasswordUpdateEncrypted:
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
