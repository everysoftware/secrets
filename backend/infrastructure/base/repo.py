import abc
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from domain.base import BaseRepository
from domain.base.repo import ReadScheme, UpdateScheme, CreateScheme
from .models import Base

SAModel = TypeVar("SAModel", bound=Base)


class SARepository(BaseRepository, abc.ABC):
    model: type[Base]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _create(self, model: SAModel) -> SAModel:
        self.session.add(model)
        return model

    async def _get(self, ident: int) -> SAModel | None:
        return await self.session.get(entity=self.model, ident=ident)

    async def _merge(self, model: SAModel) -> SAModel:
        return await self.session.merge(model)

    async def _delete(self, model: SAModel) -> None:
        return await self.session.delete(model)

    async def create(self, schema: CreateScheme) -> ReadScheme:
        model = self.model(**schema.model_dump())
        model = await self._create(model)
        await self.session.commit()
        return self.read_scheme.model_validate(model)

    async def get(self, ident: int) -> ReadScheme | None:
        model = await self._get(ident)
        return self.read_scheme.model_validate(model) if model else None

    async def update(self, ident: int, scheme: UpdateScheme) -> ReadScheme:
        model = await self._get(ident)
        model = await self._merge(model)
        await self.session.commit()
        return self.read_scheme.model_validate(model)

    async def delete(self, ident: int) -> ReadScheme:
        model = await self._get(ident)
        await self._delete(model)
        await self.session.commit()
        return self.read_scheme.model_validate(model)
