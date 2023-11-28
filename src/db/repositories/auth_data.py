from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import AuthData


class AuthDataRepo(Repository[AuthData]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=AuthData, session=session)
