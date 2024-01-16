from fastapi_pagination import Page as BasePage, Params as BaseParams
from pydantic import ConfigDict, BaseModel


class BaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Page(BasePage):
    pass


class Params(BaseParams):
    pass
