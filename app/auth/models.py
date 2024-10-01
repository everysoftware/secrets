from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Identity
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseOrm
from app.db.mixins import IDMixin, TimestampMixin


class UserOrm(BaseOrm, IDMixin, TimestampMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(default="")

    if not TYPE_CHECKING:
        id: Mapped[int] = mapped_column(Identity(), primary_key=True)
        email: Mapped[str] = mapped_column(
            String(length=320), unique=True, index=True
        )
        hashed_password: Mapped[str] = mapped_column(String(length=1024))
        is_active: Mapped[bool] = mapped_column(default=1)
        is_superuser: Mapped[bool] = mapped_column(default=0)
        is_verified: Mapped[bool] = mapped_column(default=0)
