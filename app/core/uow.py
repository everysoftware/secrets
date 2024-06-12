from __future__ import annotations

from onepattern import AlchemyUOW

from app.auth.repositories import UserRepository
from app.passwords.repositories import PasswordRepository


class UOW(AlchemyUOW):
    users: UserRepository
    passwords: PasswordRepository

    async def on_open(self) -> None:
        self.users = UserRepository(self.session)
        self.passwords = PasswordRepository(self.session)
