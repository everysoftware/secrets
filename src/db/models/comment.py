import datetime

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, str_256


class Comment(Base):
    __tablename__ = 'comments'

    record_id: Mapped[int] = mapped_column(ForeignKey(
        'records.id',
        ondelete='cascade'
    ), primary_key=True)
    text: Mapped[str_256]

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    record = relationship(
        'Record',
        back_populates='comment',
        lazy='joined',
    )
