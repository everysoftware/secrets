from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.encryption import verify_data, hash_data
from .repo import Repository
from ..models import User, AuthData


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    def new(
            self,
            user_id: int,
            first_name: str,
            last_name: str,
            auth_data: AuthData,
            language_code: str,
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
            user_id: int,
            first_name: str,
            last_name: str,
            password: str,
            master: str,
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

        return self.new(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
            auth_data=auth_data
        )

    async def login(self, user_id: int, password: str) -> bool:
        user = await self.get(user_id)

        if user is None:
            return False

        return verify_data(password, user.auth_data.account_password, user.auth_data.salt)
