from sqlalchemy import Column, VARCHAR, BigInteger
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


class Comment(Base):
    __tablename__ = 'comments'

    record_id: Mapped[int] = Column(BigInteger, ForeignKey('records.id'), primary_key=True)

    record = relationship(
        'Record',
        back_populates='comment',
        lazy='joined',
    )

    text: Mapped[str] = Column(VARCHAR(512))
