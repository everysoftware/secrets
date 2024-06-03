from typing import AsyncGenerator, Annotated

from fastapi import Depends

from secrets_app.auth.dependencies import MeDep
from secrets_app.core import UOW, Gateway, UnauthorizedGateway
from secrets_app.database.connection import async_session_factory


async def get_uow() -> AsyncGenerator[UOW, None]:
    async with UOW(async_session_factory) as uow:
        yield uow


UOWDep = Annotated[UOW, Depends(get_uow)]


async def get_unauthorized_gateway(uow: UOWDep) -> UnauthorizedGateway:
    return UnauthorizedGateway(uow)


UGWDep = Annotated[UnauthorizedGateway, Depends(get_unauthorized_gateway)]


async def get_gateway(uow: UOWDep, user: MeDep) -> Gateway:
    return Gateway(uow, user)


GWDep = Annotated[Gateway, Depends(get_gateway)]
