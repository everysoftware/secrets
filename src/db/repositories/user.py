from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from .repo import Repository


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)
