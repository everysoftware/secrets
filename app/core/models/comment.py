from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, created_at, int_pk, str_256, updated_at

if TYPE_CHECKING:
    from .record import Record


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int_pk]
    text: Mapped[str_256]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    record_id: Mapped[int] = mapped_column(ForeignKey("records.id", ondelete="cascade"))
    if TYPE_CHECKING:
        record: Record
    else:
        record: Mapped[Record] = relationship(
            back_populates="comment",
        )
