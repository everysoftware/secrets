from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.base_config import current_user
from app.bot.schemes import User
from app.core import async_session_factory
from app.core.repositories import RecordRepository
from app.core.services import RecordService


async def record_service(
        session: AsyncSession = Depends(async_session_factory),
        user: User = Depends(current_user),
) -> RecordService:
    return RecordService(RecordRepository(session), user)
