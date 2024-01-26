import datetime
from typing import Annotated

from sqlalchemy import BigInteger, Identity
from sqlalchemy.orm import mapped_column, DeclarativeBase

int_pk = Annotated[int, mapped_column(Identity(), primary_key=True)]

created_at = Annotated[
    datetime.datetime, mapped_column(default=datetime.datetime.utcnow)
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
]


class Base(DeclarativeBase):
    type_annotation_map = {int: BigInteger}
