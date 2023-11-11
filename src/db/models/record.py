import datetime
from typing import Optional

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import Identity, ForeignKey

from .base import Base, str_64


class Record(Base):
    __tablename__ = 'records'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        'users.user_id',
        ondelete='cascade'
    ))
    title: Mapped[str_64]
    username: Mapped[bytes]
    password_: Mapped[bytes]
    salt: Mapped[bytes]

    url: Mapped[Optional[str_64]]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    user = relationship(
        'User',
        back_populates='records',
    )

    comment = relationship(
        'Comment',
        back_populates='record',
        lazy='joined',
        uselist=False
    )
