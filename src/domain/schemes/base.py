import datetime
from typing import Annotated, TypeVar, Generic

from pydantic import ConfigDict, BaseModel, Field


class SBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


created_at_field = Annotated[
    datetime.datetime, Field(examples=["2021-01-01T00:00:00.000000+00:00"])
]
updated_at_field = Annotated[
    datetime.datetime, Field(examples=["2021-01-01T00:00:00.000000+00:00"])
]

T = TypeVar("T", bound=BaseModel)


class SPage(SBase, Generic[T]):
    items: list[T]


class SParams(SBase):
    limit: int = Field(100, ge=1)
    offset: int = Field(0, ge=0)
