from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.encryption import Verifying
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
            language_code: str,
            password: str,
            master: str,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
    ) -> User:
        salt = Verifying.generate_salt()
        password = Verifying.get_hash(password, salt)
        master = Verifying.get_hash(master, salt)

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

        await cache.delete(f'user_exists:{user_id}')

        return new_user

    async def authorize(self, user_id: int, password: str) -> bool:
        user = await self.get(user_id)

        if user is None:
            return False

        return Verifying.verify(password, user.auth_data.account_password, user.auth_data.salt)

    async def confirm_master(self, user_id: int, master: str) -> bool:
        user = await self.get(user_id)

        if user is None:
            raise ValueError

        master_from_db = user.auth_data.master_password
        salt = user.auth_data.salt

        return Verifying.verify(master, master_from_db, salt)
