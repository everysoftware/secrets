import datetime
from typing import Annotated

from fastapi_pagination import Page as BasePage, Params as BaseParams
from pydantic import ConfigDict, BaseModel, Field


class SBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


created_at_field = Annotated[
    datetime.datetime, Field(examples=["2021-01-01T00:00:00.000000+00:00"])
]
updated_at_field = Annotated[
    datetime.datetime, Field(examples=["2021-01-01T00:00:00.000000+00:00"])
]


class SPage(BasePage):
    pass


class SParams(BaseParams):
    pass
