from __future__ import annotations

from secrets_app.auth.repositories import UserRepository
from secrets_app.passwords.repositories import PasswordRepository
from secrets_app.skeleton.orm import BaseUOW


class UOW(BaseUOW):
    users: UserRepository
    passwords: PasswordRepository

    async def on_open(self) -> None:
        self.users = UserRepository(self.session)
        self.passwords = PasswordRepository(self.session)
