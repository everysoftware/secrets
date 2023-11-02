from typing import Optional

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.encryption import verify_data, hash_data
from src.cache import Cache
from .repo import Repository
from ..models import User, AuthData


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    def new(
            self,
            user_id: int,
            first_name: str,
            auth_data: AuthData,
            language_code: str,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
    ) -> User:
        new_user = User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            auth_data=auth_data,
            username=username,
        )
        self.session.add(new_user)
        return new_user

    async def register(
            self,
            db,
            cache: Cache,
            user_id: int,
            first_name: str,
            password: str,
            master: str,
            last_name: Optional[str] = None,
            language_code: Optional[str] = None,
            username: Optional[str] = None,
    ) -> User:
        password, salt = hash_data(password)
        master, _ = hash_data(master, salt)

        auth_data = db.auth_data.new(
            password,
            master,
            salt
        )

        new_user = self.new(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
            auth_data=auth_data
        )

        await cache.set(f'user_exists:{user_id}', '1')

        return new_user

    async def login(self, from_user: types.User, password: str) -> bool:
        user = await self.get(from_user.id)

        if user is None:
            return False

        return verify_data(password, user.auth_data.account_password, user.auth_data.salt)
