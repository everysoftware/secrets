from sqlalchemy import Column, VARCHAR, LargeBinary, BigInteger
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.schema import Identity, ForeignKey

from .base import Base


class Record(Base):
    __tablename__: str = 'records'

    id: Mapped[str] = Column(BigInteger, Identity(), primary_key=True)

    user_id: Mapped[int] = Column(BigInteger, ForeignKey('users.user_id'))
    user = relationship(
        'User',
        back_populates='records',
    )

    url: Mapped[str] = Column(VARCHAR(64), nullable=False)
    title: Mapped[str] = Column(VARCHAR(64), nullable=False)

    username: Mapped[bytes] = Column(LargeBinary)
    password_: Mapped[bytes] = Column(LargeBinary)
    salt: Mapped[bytes] = Column(LargeBinary, nullable=False)

    comment = relationship(
        'Comment',
        back_populates='record',
        lazy='joined',
        uselist=False
    )

    def __str__(self) -> str:
        return str({'id': self.id})
