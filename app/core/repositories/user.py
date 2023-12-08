from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from ..engine import async_session_factory
from ..models import User
from .base import Repository


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)


async def get_user_db(session: AsyncSession = Depends(async_session_factory)):
    yield SQLAlchemyUserDatabase(session, User)
