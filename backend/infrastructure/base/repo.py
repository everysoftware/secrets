import abc
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from domain.base import BaseRepository
from domain.base.repo import Schema, CreateScheme, UpdateScheme
from .models import Base

SAModel = TypeVar("SAModel", bound=Base)


class SARepository(BaseRepository, abc.ABC):
    model: type[Base]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_model(self, ident: int) -> SAModel | None:
        return await self.session.get(entity=self.model, ident=ident)

    async def update_model(self, model: SAModel) -> SAModel:
        return await self.session.merge(model)

    async def create(self, scheme: CreateScheme) -> Schema:
        model = self.model(**scheme.model_dump())
        self.session.add(model)
        await self.session.commit()

        return self.scheme.model_validate(model)

    async def get(self, ident: int) -> Schema | None:
        model = await self.get_model(ident)

        return self.scheme.model_validate(model) if model else None

    async def update(self, ident: int, scheme: UpdateScheme) -> Schema:
        model = await self.get_model(ident)

        for key in scheme.model_fields.keys():
            if getattr(scheme, key) is not None:
                setattr(model, key, getattr(scheme, key))

        model = await self.session.merge(model)

        await self.session.commit()

        return self.scheme.model_validate(model)

    async def delete(self, ident: int) -> Schema:
        model = await self.get_model(ident)
        await self.session.delete(model)

        await self.session.commit()

        return self.scheme.model_validate(model)
