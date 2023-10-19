from sqlalchemy.ext.asyncio import AsyncSession

from src.encryption import verify_data
from .repo import Repository
from ..models import User, AuthData


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    def new(
            self,
            user_id: int,
            username: str,
            account: AuthData,
    ) -> User:
        new_user = User(
            user_id=user_id,
            username=username,
            auth_data=account,
        )
        self.session.add(new_user)
        return new_user

    async def login(self, user_id: int, password: str) -> bool:
        user = await self.get(user_id)

        if user is None:
            return False

        return verify_data(password, user.auth_data.account_password, user.auth_data.salt)
