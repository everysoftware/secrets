from domain.schemes import UserScheme
from infrastructure.utils import generate_secret
from .base import Service


class UserService(Service):
    async def enable_2fa(self, user: UserScheme) -> UserScheme:
        async with self.uow:
            model = await self.uow.users.get(user.id)
            model.is_2fa_enabled = True
            await self.uow.users.update(model)

            return UserScheme.model_validate(model)

    async def update_otp_secret(self, user: UserScheme) -> UserScheme:
        async with self.uow:
            model = await self.uow.users.get(user.id)
            model.otp_secret = generate_secret()
            await self.uow.users.update(model)

            return UserScheme.model_validate(model)
