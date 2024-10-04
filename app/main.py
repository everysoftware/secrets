from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.config import settings
from app.cors import setup_cors
from app.routing import main_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup tasks
    # ...
    yield
    # Shutdown tasks
    # ...


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_display_name,
    version=settings.app_version,
    root_path=settings.app_root_path,
)
setup_cors(app)

app.include_router(main_router)
