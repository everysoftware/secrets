from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces import IUnitOfWork
from infrastructure.database import async_session_factory
from infrastructure.repositories import UserRepository, PasswordRepository


class UnitOfWork(IUnitOfWork):
    session: AsyncSession

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
