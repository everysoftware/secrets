from typing import TypeVar, Generic, Sequence, Protocol

from sqlalchemy import select, func, ColumnElement, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import BaseOrm

SAModel = TypeVar("SAModel", bound=BaseOrm)


class EntityNotFound(ValueError):
    """Entity not found in the database."""

    def __init__(self, ident: int) -> None:
        self.ident = ident
        super().__init__(f"Entity with id {ident} not found.")


class Repository(Protocol):
    pass


class SARepository(Repository, Generic[SAModel]):
    model: type[SAModel]
    """Database model."""
    session: AsyncSession
    """Database session."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: SAModel) -> None:
        """Create a new model in the database."""
        self.session.add(model)

    async def get_or_none(self, ident: int) -> SAModel | None:
        """Get a model from the database. Return `None` if not found."""
        return await self.session.get(entity=self.model, ident=ident)

    async def get(self, ident: int) -> SAModel:
        """Get a model from the database. Raise `EntityNotFound` if not found."""
        model = await self.get_or_none(ident)

        if model is None:
            raise EntityNotFound(ident)

        return model

    async def update(self, model: SAModel) -> SAModel:
        """Update a model in the database."""
        return await self.session.merge(model)

    async def delete(self, model: SAModel) -> None:
        """Delete a model from the database."""
        await self.session.delete(model)

    async def count(self, *args: ColumnElement[bool]) -> int:
        """Count models in the database."""
        stmt = select(func.count(self.model)).where(*args)
        res = await self.session.execute(stmt)
        count = res.scalar_one()

        return count

    async def get_many(
        self,
        *,
        where: Sequence[BinaryExpression[bool] | ColumnElement[bool]] = (),
        order_by: Sequence[ColumnElement[bool]] = (),
        limit: int = 10,
        offset: int = 0,
    ) -> list[SAModel]:
        """Get many models in the database."""
        stmt = (
            select(self.model)
            .where(*where)
            .order_by(*order_by)
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(stmt)

        return list(res.scalars().all())
