from typing import Optional

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, str_256


class Comment(Base):
    __tablename__ = 'comments'

    record_id: Mapped[int] = mapped_column(ForeignKey('records.id'), primary_key=True)

    record = relationship(
        'Record',
        back_populates='comment',
        lazy='joined',
    )

    text: Mapped[Optional[str_256]]
