from domain.user import BaseUserRepository, UserUpdate, UserScheme
from infrastructure.auth import generate_secret


class UserService:
    repository: BaseUserRepository

    def __init__(self, repository: BaseUserRepository):
        self.repository = repository

    async def enable_2fa(self) -> UserScheme:
        return await self.repository.enable_2fa()

    async def update_otp_secret(self) -> UserScheme:
        return await self.repository.update_otp_secret(generate_secret())
