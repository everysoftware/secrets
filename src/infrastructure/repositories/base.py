from typing import TypeVar, Generic, Sequence, Protocol

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, func, UnaryExpression
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.infrastructure.models import BaseOrm
from src.domain.schemes import SParams, SPage, SPasswordItem

SAModel = TypeVar("SAModel", bound=BaseOrm)


class Repository(Protocol):
    pass


class SARepository(Repository, Generic[SAModel]):
    model: type[BaseOrm]
    """Модель базы данных."""
    session: AsyncSession
    """Сессия базы данных."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: SAModel) -> None:
        """Добавление модели в базу данных."""
        self.session.add(model)

    async def get(self, ident: int) -> SAModel | None:
        """Получение модели из базы данных по идентификатору."""
        return await self.session.get(entity=self.model, ident=ident)

    async def update(self, model: SAModel) -> SAModel:
        """Обновление модели в базе данных."""
        return await self.session.merge(model)

    async def delete(self, model: SAModel) -> None:
        """Удаление модели из базы данных."""
        await self.session.delete(model)

    async def count(self, *args) -> int:
        """Получение количества моделей в базе данных."""
        stmt = select(func.count(self.model)).where(*args)
        res = await self.session.execute(stmt)
        count = res.scalar_one()

        return count

    async def search(
        self,
        params: SParams,
        *,
        where: Sequence[ORMOption] | None = None,
        order_by: Sequence[UnaryExpression] | None = None
    ) -> SPage[SPasswordItem]:
        """Поиск моделей в базе данных."""
        stmt = select(self.model).where(*where).order_by(*order_by)
        page = await paginate(self.session, stmt, params)

        return page
