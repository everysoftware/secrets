import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, func, Identity
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class UserOrm(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(server_default="")
    is_active: Mapped[bool] = mapped_column(server_default="true")
    is_superuser: Mapped[bool] = mapped_column(server_default="false")
    is_verified: Mapped[bool] = mapped_column(server_default="false")
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
