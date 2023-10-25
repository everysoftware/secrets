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
    user = relationship(
        'User',
        back_populates='records',
    )

    url: Mapped[str_64]
    title: Mapped[str_64]

    username: Mapped[bytes]
    password_: Mapped[bytes]
    salt: Mapped[bytes]

    comment = relationship(
        'Comment',
        back_populates='record',
        lazy='joined',
        uselist=False
    )
