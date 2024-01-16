from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.base import Page, Params
from domain.password import BasePasswordRepository, PasswordItem
from domain.password import PasswordCreate, PasswordRead, PasswordUpdate
from infrastructure.base import SARepository
from infrastructure.user import User
from .models import Password


class PasswordRepository(BasePasswordRepository, SARepository):
    model = Password

    def __init__(self, session: AsyncSession, user: User):
        super().__init__(session)
        self.user = user

    async def _get(self, ident: int) -> Password | None:
        return await self.session.get(
            entity=self.model,
            ident=ident,
            options=[joinedload(Password.comment)],  # noqa E501
        )

    async def create(self, schema: PasswordCreate) -> PasswordRead:
        model = Password(**schema.model_dump(), user_id=self.user.id, comment=None)
        record = await self._create(model)
        await self.session.commit()
        return PasswordRead.model_validate(record)

    async def update(self, ident: int, schema: PasswordUpdate) -> PasswordRead:
        model = await self._get(ident)

        if schema.name is not None:
            model.name = schema.name

        if schema.username is not None:
            model.username = schema.username

        if schema.password is not None:
            model.password = schema.password

        if schema.url is not None:
            model.url = schema.url

        model = await self._merge(model)

        return PasswordRead.model_validate(model)

    async def count(self) -> int:
        stmt = select(func.count(Password.id)).where(Password.owner_id == self.user.id)
        res = await self.session.execute(stmt)
        count = res.scalar_one()

        return count

    async def search(self, params: Params) -> Page[PasswordItem]:
        stmt = (
            select(Password)
            .where(Password.owner_id == self.user.id)
            .order_by(Password.name)
            .options(joinedload(Password.comment))  # noqa E501
        )

        return await paginate(self.session, stmt, params)
