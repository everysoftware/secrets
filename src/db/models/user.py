import datetime
from typing import Optional

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import Identity

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Identity(), unique=True)

    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    auth_data = relationship(
        'AuthData',
        back_populates='user',
        uselist=False,
        lazy='joined',
    )

    reg_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())

    records = relationship(
        'Record',
        back_populates='user',
        lazy='selectin',
        order_by='Record.title'
    )
