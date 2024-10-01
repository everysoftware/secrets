from __future__ import annotations

from typing import Any, cast, Self

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncSessionTransaction,
)

from app.auth.repositories import UserRepository
from app.passwords.repositories import PasswordRepository


class UOW:
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession
    transaction: AsyncSessionTransaction

    users: UserRepository
    passwords: PasswordRepository

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    @property
    def is_active(self) -> bool:
        if not self.session:
            return False
        return cast(bool, self.session.is_active)

    async def on_after_begin(self) -> None:
        self.users = UserRepository(self.session)
        self.passwords = PasswordRepository(self.session)

    async def begin(self) -> None:
        self.session = self.session_factory()
        await self.session.__aenter__()
        self.transaction = self.session.begin()
        await self.transaction.__aenter__()
        await self.on_after_begin()

    async def close(self, type_: Any, value: Any, traceback: Any) -> None:
        await self.transaction.__aexit__(type_, value, traceback)
        await self.session.__aexit__(type_, value, traceback)

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def __aenter__(self) -> Self:
        await self.begin()
        return self

    async def __aexit__(self, type_: Any, value: Any, traceback: Any) -> None:
        await self.close(type_, value, traceback)
