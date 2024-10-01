from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from app.db.base import BaseOrm
from app.db.mixins import TimestampMixin, IDMixin


class PasswordOrm(BaseOrm, IDMixin, TimestampMixin):
    __tablename__ = "passwords"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    name: Mapped[str]
    encrypted_username: Mapped[str]
    encrypted_password: Mapped[str]
    url: Mapped[str] = mapped_column(default="")
    note: Mapped[str] = mapped_column(default="")
