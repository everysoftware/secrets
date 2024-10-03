from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.auth_router import router as auth_router
from app.auth.user_router import router as users_router
from app.config import settings
from app.passwords.router import router as passwords_router

# Routers
routers = [auth_router, passwords_router, users_router]


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup tasks
    # ...
    yield
    # Shutdown tasks
    # ...


app = FastAPI(
    lifespan=lifespan,
    title=settings.app.title,
    version=settings.app.version,
    root_path=settings.app.root_path,
)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=settings.app.cors_origins,
    allow_credentials=True,
    allow_methods=settings.app.cors_methods,
    allow_headers=settings.app.cors_headers,
)

for router in routers:
    app.include_router(router)


@app.get("/hc", include_in_schema=False)
def hc() -> dict[str, Any]:
    return {"status": "ok"}
