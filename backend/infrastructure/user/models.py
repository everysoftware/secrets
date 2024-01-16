from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from infrastructure.base.models import Base, created_at, int_pk, updated_at

if TYPE_CHECKING:
    from infrastructure.password.models import Password


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    is_two_fa_enabled: Mapped[bool] = False
    secret_otp: Mapped[str | None]

    if TYPE_CHECKING:
        passwords: list[Password]
    else:
        passwords: Mapped[list[Password]] = relationship(
            back_populates="owner", cascade="delete", order_by="Password.name"
        )
