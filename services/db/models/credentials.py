from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, created_at, int_pk, str_64, updated_at

if TYPE_CHECKING:
    from .user import User


class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[int_pk]
    password: Mapped[str_64]
    master_password: Mapped[str_64]
    salt: Mapped[bytes]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    user: Mapped[User] = relationship(
        back_populates="credentials",
    )
