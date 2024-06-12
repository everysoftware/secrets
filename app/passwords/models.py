from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from app.models import EntityBase


class PasswordOrm(EntityBase):
    __tablename__ = "passwords"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    title: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    url: Mapped[str] = mapped_column(server_default="")
    note: Mapped[str] = mapped_column(server_default="")
