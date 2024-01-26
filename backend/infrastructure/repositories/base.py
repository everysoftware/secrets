from abc import ABC
from typing import TypeVar, Sequence, Generic

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from common.settings import settings
from domain.repositories import IRepository
from domain.schemes import Params, Page
from domain.schemes.dtos import PasswordItem
from infrastructure.models import Base
from infrastructure.utils import aes

SAModel = TypeVar("SAModel", bound=Base)


class SARepository(Generic[SAModel], IRepository, ABC):
    model: type[Base]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: SAModel) -> None:
        self.session.add(model)

    async def get(self, ident: int) -> SAModel | None:
        return await self.session.get(entity=self.model, ident=ident)

    async def update(self, model: SAModel) -> SAModel:
        return await self.session.merge(model)

    async def delete(self, model: SAModel) -> None:
        await self.session.delete(model)

    async def count(self, *args) -> int:
        stmt = select(func.count(self.model)).where(*args)
        res = await self.session.execute(stmt)
        count = res.scalar_one()

        return count

    async def search(
            self,
            params: Params,
            *,
            where: Sequence | None = None,
            order_by: Sequence | None = None
    ) -> Page[PasswordItem]:
        stmt = select(self.model).where(*where).order_by(*order_by)
        page = await paginate(self.session, stmt, params)

        for item in page.items:
            item.username = aes.decrypt(item.username, settings.infrastructure.encryption.secret)

        return page
