from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, str_64, created_at, int_pk, updated_at

if TYPE_CHECKING:
    from .user import User
    from .comment import Comment


class Record(Base):
    __tablename__ = 'records'

    id: Mapped[int_pk]
    title: Mapped[str_64]
    username: Mapped[bytes]
    password_: Mapped[bytes]
    salt: Mapped[bytes]
    url: Mapped[str_64 | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_id: Mapped[int] = mapped_column(ForeignKey(
        'users.id',
        ondelete='cascade'
    ))
    user: Mapped[User] = relationship(
        back_populates='records',
    )
    comment: Mapped[Comment] = relationship(
        back_populates='record',
        cascade='delete'
    )
