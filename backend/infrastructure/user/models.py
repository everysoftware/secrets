from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.base.models import Base, created_at, int_pk, updated_at


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    is_2fa_enabled: Mapped[bool] = mapped_column(default=False)
    otp_secret: Mapped[str | None]
