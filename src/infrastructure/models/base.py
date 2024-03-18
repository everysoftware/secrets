import datetime
from typing import Annotated

from sqlalchemy import BigInteger, Identity, MetaData
from sqlalchemy.orm import mapped_column, DeclarativeBase

int_pk = Annotated[int, mapped_column(Identity(), primary_key=True)]

created_at = Annotated[
    datetime.datetime, mapped_column(default=datetime.datetime.utcnow)
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
]

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class BaseOrm(DeclarativeBase):
    __abstract__ = True
    type_annotation_map = {int: BigInteger}
    metadata = metadata

    def get_or_raise(self, key: str):
        return getattr(self, key)
