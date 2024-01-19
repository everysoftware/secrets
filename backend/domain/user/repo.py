import abc

from domain.base.repo import BaseRepository
from domain.user.schemes import UserScheme, UserCreate, UserUpdate


class BaseUserRepository(BaseRepository, abc.ABC):
    scheme = UserScheme
    create_scheme = UserCreate
    update_scheme = UserUpdate

    async def enable_2fa(self) -> UserScheme:
        ...

    async def update_otp_secret(self, secret: str) -> UserScheme:
        ...
