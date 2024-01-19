from sqlalchemy.ext.asyncio import AsyncSession

from domain.user import BaseUserRepository, UserScheme
from infrastructure.base import SARepository
from .models import User


class UserRepository(BaseUserRepository, SARepository):
    model = User

    def __init__(self, session: AsyncSession, user: User):
        super().__init__(session)
        self.user = user

    async def enable_2fa(self) -> UserScheme:
        self.user.otp_secret = None
        return UserScheme.model_validate(await self.update_model(self.user))

    async def update_otp_secret(self, secret: str) -> UserScheme:
        self.user.otp_secret = secret
        return UserScheme.model_validate(await self.update_model(self.user))
