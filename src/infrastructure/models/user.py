from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users.models import ID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseOrm, int_pk, created_at, updated_at

if TYPE_CHECKING:
    from .password import PasswordOrm


class UserOrm(SQLAlchemyBaseUserTable[int], BaseOrm):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    first_name: Mapped[str]
    last_name: Mapped[str]
    two_factor: Mapped[bool] = mapped_column(default=False)
    otp_secret: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    if TYPE_CHECKING:
        id: ID
        email: str
        hashed_password: str
        is_active: bool
        is_superuser: bool
        is_verified: bool
        passwords: list[PasswordOrm]
    else:
        passwords: Mapped[list[PasswordOrm]] = relationship(back_populates="user")
