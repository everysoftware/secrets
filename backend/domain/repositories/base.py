from abc import ABC
from typing import TypeVar

from domain.schemes.base import BaseScheme

Schema = TypeVar("Schema", bound=BaseScheme)
CreateScheme = TypeVar("CreateScheme", bound=BaseScheme)
UpdateScheme = TypeVar("UpdateScheme", bound=BaseScheme)


class IRepository(ABC):
    scheme: type[BaseScheme]
    create_scheme: type[BaseScheme]
    update_scheme: type[BaseScheme]
