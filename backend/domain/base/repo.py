import abc
from typing import TypeVar

from pydantic import BaseModel

ReadScheme = TypeVar("ReadScheme", bound=BaseModel)
CreateScheme = TypeVar("CreateScheme", bound=BaseModel)
UpdateScheme = TypeVar("UpdateScheme", bound=BaseModel)


class BaseRepository(abc.ABC):
    read_scheme: type[BaseModel]
    create_scheme: type[BaseModel]
    update_scheme: type[BaseModel]

    @abc.abstractmethod
    async def create(self, schema: CreateScheme) -> ReadScheme:
        pass

    @abc.abstractmethod
    async def get(self, ident: int) -> ReadScheme | None:
        ...

    @abc.abstractmethod
    async def update(self, ident: int, schema: UpdateScheme) -> ReadScheme:
        ...

    @abc.abstractmethod
    async def delete(self, ident: int) -> ReadScheme:
        ...
