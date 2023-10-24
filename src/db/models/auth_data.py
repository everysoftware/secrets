from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, str_64


class AuthData(Base):
    __tablename__ = 'auth_data'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    """Telegram User ID"""
    user = relationship(
        'User',
        back_populates='auth_data',
    )

    account_password: Mapped[str_64]
    master_password: Mapped[str_64]
    salt: Mapped[bytes]
