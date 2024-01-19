from application.config import app_settings as app_settings
from domain.base import Page, Params
from domain.password import (
    BasePasswordRepository,
    PasswordSettings,
    PasswordCreate,
    PasswordScheme,
    PasswordUpdate,
    PasswordItem,
)
from infrastructure.password import password_generator
from infrastructure.security import aes


class PasswordService:
    def __init__(self, repo: BasePasswordRepository):
        self.repository = repo

    async def create(self, scheme: PasswordCreate) -> PasswordScheme:
        scheme.username = aes.encrypt(scheme.username, app_settings.encryption.secret)
        scheme.password = aes.encrypt(scheme.password, app_settings.encryption.secret)

        return await self.repository.create(scheme)

    async def get(self, ident: int) -> PasswordScheme | None:
        return await self.repository.get(ident)

    async def search(self, params: Params) -> Page[PasswordItem]:
        return await self.repository.search(params)

    async def update(self, ident: int, scheme: PasswordUpdate) -> PasswordScheme:
        if scheme.username is not None:
            scheme.username = aes.encrypt(
                scheme.username, app_settings.encryption.secret
            )

        if scheme.password is not None:
            scheme.password = aes.encrypt(
                scheme.password, app_settings.encryption.secret
            )

        return await self.repository.update(ident, scheme)

    async def delete(self, ident: int) -> PasswordScheme:
        return await self.repository.delete(ident)

    @staticmethod
    async def generate(settings: PasswordSettings) -> str:
        return password_generator.generate(settings)
