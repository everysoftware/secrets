import datetime
from typing import Annotated

from sqlalchemy import BigInteger, String, Identity
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(Identity(), primary_key=True)]

str_64 = Annotated[str, 64]
str_256 = Annotated[str, 256]

created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow)]
updated_at = Annotated[datetime.datetime, mapped_column(
    default=datetime.datetime.utcnow,
    onupdate=datetime.datetime.utcnow
)]


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BigInteger,
        str_64: String(64),
        str_256: String(256)
    }
