from typing import AsyncGenerator, Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.models import UserOrm
from .backends import cookie_jwt_backend
from .manager import UserManager
from .schemas import SUserRead
from ..db.connection import async_session_factory


async def get_user_db() -> (
    AsyncGenerator[SQLAlchemyUserDatabase[UserOrm, int], None]
):
    async with async_session_factory() as session:
        yield SQLAlchemyUserDatabase(session, UserOrm)


async def get_user_manager(
    user_db: Annotated[
        SQLAlchemyUserDatabase[UserOrm, int], Depends(get_user_db)
    ],
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[UserOrm, int](
    get_user_manager,
    [cookie_jwt_backend],
)

current_user = fastapi_users.current_user()


def get_me(user: UserOrm = Depends(current_user)) -> SUserRead:
    return SUserRead.model_validate(user)


MeDep = Annotated[SUserRead, Depends(get_me)]
