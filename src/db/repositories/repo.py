from typing import Generic, TypeVar, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from ..models import Base

AbstractModel = TypeVar('AbstractModel')


class Repository(Generic[AbstractModel]):
    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str, options: Sequence[ORMOption] | None = None) -> AbstractModel:
        return await self.session.get(entity=self.type_model, ident=ident, options=options)

    async def get_by_where(self, where_clause) -> AbstractModel | None:
        statement = select(self.type_model).where(where_clause)
        return (await self.session.execute(statement)).one_or_none()

    async def delete(self, model: AbstractModel) -> None:
        return await self.session.delete(model)

    async def merge(self, model: AbstractModel) -> AbstractModel:
        return await self.session.merge(model)

    def new(self, model: AbstractModel) -> AbstractModel:
        self.session.add(model)
        return model
