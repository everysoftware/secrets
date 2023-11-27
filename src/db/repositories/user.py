from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import User


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)
