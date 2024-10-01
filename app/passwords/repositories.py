from sqlalchemy import select

from app.db.repository import AlchemyRepository
from app.db.schemas import Page, PageParams
from app.db.types import ID
from app.passwords.models import PasswordOrm
from app.passwords.schemas import SPasswordDB


class PasswordRepository(AlchemyRepository[PasswordOrm, SPasswordDB]):
    model_type = PasswordOrm
    schema_type = SPasswordDB

    async def search(
        self, user_id: ID, params: PageParams, *, query: str | None = None
    ) -> Page[SPasswordDB]:
        stmt = select(self.model_type).where(
            self.model_type.user_id == user_id  # noqa
        )
        if query is not None:
            stmt = stmt.where(self.model_type.name.ilike(f"%{query}%"))
        stmt = self.build_pagination_query(params, stmt)
        result = await self.session.scalars(stmt)
        return self.validate_page(result)
