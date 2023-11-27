from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, str_64, int_pk, created_at, updated_at

if TYPE_CHECKING:
    from .user import User


class AuthData(Base):
    __tablename__ = 'auth_data'

    id: Mapped[int_pk]
    account_password: Mapped[str_64]
    master_password: Mapped[str_64]
    salt: Mapped[bytes]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_id: Mapped[int] = mapped_column(ForeignKey(
        'users.id',
        ondelete='cascade'
    ))
    user: Mapped[User] = relationship(
        back_populates='auth_data',
    )
