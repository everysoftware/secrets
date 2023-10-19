from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import AuthData


class AuthDataRepo(Repository[AuthData]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=AuthData, session=session)

    def new(
            self,
            account_password: str,
            master_password: str,
            salt: bytes,
    ) -> AuthData:
        new_data = AuthData(
            account_password=account_password,
            master_password=master_password,
            salt=salt,
        )
        self.session.add(new_data)
        return new_data
