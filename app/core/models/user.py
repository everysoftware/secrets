from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..enums import UserRole
from .base import Base, created_at, int_pk, updated_at

if TYPE_CHECKING:
    from .record import Record


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    language_code: Mapped[str | None]
    username: Mapped[str | None]
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    hashed_master: Mapped[str]

    if TYPE_CHECKING:
        records: list[Record]
    else:
        records: Mapped[list[Record]] = relationship(
            back_populates="user", cascade="delete", order_by="Record.name"
        )
