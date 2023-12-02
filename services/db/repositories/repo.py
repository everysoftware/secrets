from typing import Generic, Sequence, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from ..models import Base

AbstractModel = TypeVar("AbstractModel", bound=Base)


class Repository(Generic[AbstractModel]):
    type_model: type[AbstractModel]
    session: AsyncSession

    def __init__(self, type_model: type[AbstractModel], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(
        self, ident: int | str, options: Sequence[ORMOption] | None = None
    ) -> AbstractModel | None:
        return await self.session.get(
            entity=self.type_model, ident=ident, options=options
        )

    async def get_by_where(self, where_clause) -> AbstractModel | None:
        raise NotImplementedError

    async def delete(self, model: AbstractModel) -> None:
        return await self.session.delete(model)

    async def merge(self, model: AbstractModel) -> AbstractModel:
        return await self.session.merge(model)

    def new(self, model: AbstractModel) -> AbstractModel:
        self.session.add(model)
        return model
