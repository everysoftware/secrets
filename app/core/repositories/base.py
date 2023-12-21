import abc
from typing import Generic, Sequence, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from ..models import Base

AbstractModel = TypeVar("AbstractModel", bound=Base)


class SQLAlchemyRepository(Generic[AbstractModel], abc.ABC):
    model: type[Base]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
            self, ident: int | str, options: Sequence[ORMOption] | None = None
    ) -> AbstractModel | None:
        return await self.session.get(entity=self.model, ident=ident, options=options)

    async def delete(self, model: AbstractModel) -> None:
        return await self.session.delete(model)

    async def merge(self, model: AbstractModel) -> AbstractModel:
        return await self.session.merge(model)

    def new(self, model: AbstractModel) -> AbstractModel:
        self.session.add(model)
        return model
