import abc
from typing import TypeVar

from .schemes import BaseScheme

Schema = TypeVar("Schema", bound=BaseScheme)
CreateScheme = TypeVar("CreateScheme", bound=BaseScheme)
UpdateScheme = TypeVar("UpdateScheme", bound=BaseScheme)


class BaseRepository(abc.ABC):
    scheme: type[BaseScheme]
    create_scheme: type[BaseScheme]
    update_scheme: type[BaseScheme]

    @abc.abstractmethod
    async def create(self, schema: CreateScheme) -> Schema:
        pass

    @abc.abstractmethod
    async def get(self, ident: int) -> Schema | None:
        ...

    @abc.abstractmethod
    async def update(self, ident: int, schema: UpdateScheme) -> Schema:
        ...

    @abc.abstractmethod
    async def delete(self, ident: int) -> Schema:
        ...
