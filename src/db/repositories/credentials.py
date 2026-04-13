from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Credentials
from .repo import Repository


class CredentialsRepo(Repository[Credentials]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Credentials, session=session)
