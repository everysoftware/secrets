import datetime

from sqlalchemy import Identity
from sqlalchemy.orm import mapped_column, Mapped

from app.db import utils
from app.db.types import ID


class Mixin:
    pass


class IDMixin(Mixin):
    id: Mapped[ID] = mapped_column(
        Identity(),
        primary_key=True,
        sort_order=-100,
    )


class TimestampMixin(Mixin):
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=utils.naive_utc, sort_order=100
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=utils.naive_utc,
        onupdate=utils.naive_utc,
        sort_order=101,
    )
