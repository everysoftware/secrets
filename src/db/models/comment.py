from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, str_256, int_pk, created_at, updated_at

if TYPE_CHECKING:
    from .record import Record


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int_pk]
    text: Mapped[str_256]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    record_id: Mapped[int] = mapped_column(ForeignKey(
        'records.id',
        ondelete='cascade'
    ))
    record: Mapped[Record] = relationship(
        back_populates='comment',
    )
