from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.base import Page, Params
from domain.password import BasePasswordRepository, PasswordItem
from domain.password import PasswordCreate, PasswordScheme
from infrastructure.base import SARepository
from infrastructure.user import User
from .models import Password


class PasswordRepository(BasePasswordRepository, SARepository):
    model = Password

    def __init__(self, session: AsyncSession, user: User):
        super().__init__(session)
        self.user = user

    async def create(self, schema: PasswordCreate) -> PasswordScheme:
        model = self.model(**schema.model_dump(), owner_id=self.user.id)
        self.session.add(model)
        await self.session.commit()
        return self.scheme.model_validate(model)

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
        )

        return await paginate(self.session, stmt, params)
