from common.settings import settings
from domain.schemes.base import (
    Page,
    Params,
)
from domain.schemes.entities import (
    PasswordScheme,
    UserScheme,
)
from domain.schemes.transfer import (
    PasswordCreate,
    PasswordItem,
    PasswordSettings,
    PasswordUpdate,
    EncryptedPassword,
)
from infrastructure.models import Password
from infrastructure.utils import password_generator, aes
from .base import Service


class PasswordService(Service):
    async def create(self, user: UserScheme, scheme: PasswordCreate) -> PasswordScheme:
        model = Password(**scheme.model_dump())

        model.user_id = user.id
        model.username = aes.encrypt(
            scheme.username, settings.infrastructure.encryption.secret
        )
        model.password = aes.encrypt(
            scheme.password, settings.infrastructure.encryption.secret
        )

        async with self.uow:
            await self.uow.passwords.create(model)

        return await self.get(model.id)

    async def get(self, ident: int) -> PasswordScheme | None:
        async with self.uow:
            model = await self.uow.passwords.get(ident)

        if model is None:
            return None

        encrypted_scheme = EncryptedPassword.model_validate(model)

        dump = encrypted_scheme.model_dump()
        dump["username"] = aes.decrypt(
            encrypted_scheme.username, settings.infrastructure.encryption.secret
        )
        dump["password"] = aes.decrypt(
            encrypted_scheme.password, settings.infrastructure.encryption.secret
        )

        scheme = PasswordScheme(**dump)

        return scheme

    async def search(
        self, user: UserScheme, params: Params, query: str | None = None
    ) -> Page[PasswordItem]:
        where = [Password.user_id == user.id]
        if query is not None:
            where.append(Password.name.ilike(f"%{query}%"))

        async with self.uow:
            return await self.uow.passwords.search(
                params,
                where=where,
                order_by=[Password.name.asc()],
            )

    async def update(
        self, scheme: PasswordScheme, update_scheme: PasswordUpdate
    ) -> PasswordScheme:
        async with self.uow:
            model = await self.uow.passwords.get(scheme.id)

            for name, value in update_scheme.model_dump(
                exclude_unset=True, exclude={"username", "password"}
            ).items():
                setattr(model, name, value)

            if update_scheme.username is not None:
                model.username = aes.encrypt(
                    update_scheme.username, settings.infrastructure.encryption.secret
                )

            if update_scheme.password is not None:
                model.password = aes.encrypt(
                    update_scheme.password, settings.infrastructure.encryption.secret
                )

            await self.uow.passwords.update(model)

        return await self.get(model.id)

    async def delete(self, scheme: PasswordScheme) -> None:
        async with self.uow:
            model = await self.uow.passwords.get(scheme.id)
            await self.uow.passwords.delete(model)

    @staticmethod
    async def generate(password_settings: PasswordSettings) -> str:
        return password_generator.generate(password_settings)
