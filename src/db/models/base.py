from typing import Annotated

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase

str_64 = Annotated[str, 64]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BigInteger,
        str_64: String(64),
        str_256: String(256)
    }

# Base = declarative_base()
