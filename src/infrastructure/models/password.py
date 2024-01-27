from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, created_at, int_pk, updated_at

if TYPE_CHECKING:
    from .user import User


class Password(Base):
    __tablename__ = "passwords"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    url: Mapped[str | None]
    comment: Mapped[str | None]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    if TYPE_CHECKING:
        user: User
    else:
        user: Mapped[User] = relationship(
            back_populates="passwords",
        )
