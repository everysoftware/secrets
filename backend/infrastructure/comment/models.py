from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from infrastructure.base.models import Base, created_at, str_256, updated_at
from infrastructure.password import Password


class Comment(Base):
    __tablename__ = "comments"

    password_id: Mapped[int] = mapped_column(
        ForeignKey("passwords.id", ondelete="cascade"),
        primary_key=True,
    )
    text: Mapped[str_256]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    if TYPE_CHECKING:
        password: Password
    else:
        password: Mapped[Password] = relationship(
            back_populates="comment",
        )
