import abc
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar('AbstractModel')


class Repository(Generic[AbstractModel]):
    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, where_clause) -> AbstractModel | None:
        statement = select(self.type_model).where(where_clause)
        return (await self.session.execute(statement)).one_or_none()

    async def get_many(
            self, where_clause, limit: int = 100, order_by=None
    ) -> Sequence[Base]:
        statement = select(self.type_model).where(where_clause).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(self, where_clause) -> None:
        statement = delete(self.type_model).where(where_clause)
        await self.session.execute(statement)

    async def merge(self, model: AbstractModel) -> AbstractModel:
        return await self.session.merge(model)

    @abc.abstractmethod
    def new(self, *args, **kwargs) -> None:
        ...
