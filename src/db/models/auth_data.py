from sqlalchemy import Column, VARCHAR, LargeBinary, BigInteger
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


class AuthData(Base):
    __tablename__ = 'auth_data'

    user_id: Mapped[int] = Column(BigInteger, ForeignKey('users.user_id'), primary_key=True)
    """Telegram User ID"""
    user = relationship(
        'User',
        back_populates='auth_data',
    )

    account_password: Mapped[str] = Column(VARCHAR(64), nullable=False)
    master_password: Mapped[str] = Column(VARCHAR(64), nullable=False)
    salt: Mapped[bytes] = Column(LargeBinary, nullable=False)
