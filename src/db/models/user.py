import datetime

from sqlalchemy import Column, VARCHAR, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.schema import Identity

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(BigInteger, Identity(), unique=True)

    user_id: Mapped[int] = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    """Telegram User ID"""

    username: Mapped[str] = Column(VARCHAR(32), unique=True, nullable=False)
    auth_data = relationship(
        'AuthData',
        back_populates='user',
        uselist=False,
        lazy='joined',
    )

    reg_date: Mapped[datetime] = Column(TIMESTAMP, default=datetime.datetime.now(), nullable=False)

    records = relationship(
        'Record',
        back_populates='user',
        lazy='selectin',
    )

    def __str__(self) -> str:
        return str({'id': self.id})
