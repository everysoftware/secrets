from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from infrastructure.base.models import Base, created_at, int_pk, updated_at
from infrastructure.user.models import User


class Password(Base):
    __tablename__ = "passwords"

    id: Mapped[int_pk]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    url: Mapped[str | None]
    comment: Mapped[str | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    if TYPE_CHECKING:
        owner: User
    else:
        owner: Mapped[User] = relationship()
