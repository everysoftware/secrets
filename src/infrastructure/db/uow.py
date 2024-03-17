from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.connection import async_session_factory
from src.infrastructure.repositories import UserRepository, PasswordRepository


class UnitOfWork:
    session: AsyncSession
    users: UserRepository
    passwords: PasswordRepository

    def __init__(self):
        self.session_factory = async_session_factory

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.passwords = PasswordRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.commit()
