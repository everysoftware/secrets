from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, created_at, int_pk, str_64, updated_at

if TYPE_CHECKING:
    from .comment import Comment
    from .user import User


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int_pk]
    title: Mapped[str_64]
    username: Mapped[bytes]
    password: Mapped[bytes]
    salt: Mapped[bytes]
    url: Mapped[str_64 | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    user: Mapped[User] = relationship(
        back_populates="records",
    )
    comment: Mapped[Comment] = relationship(back_populates="record", cascade="delete")
