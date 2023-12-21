from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from ..engine import async_session_factory
from ..models import User


class UserRepository(SQLAlchemyRepository[User]):
    model = User


async def get_user_db(session: AsyncSession = Depends(async_session_factory)):
    yield SQLAlchemyUserDatabase(session, User)
