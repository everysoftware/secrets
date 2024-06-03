from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from secrets_app.auth.router import router as auth_router
from secrets_app.passwords.router import router as passwords_router
from secrets_app.settings import settings
from secrets_app.users.router import router as users_router

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
    summary="A powerful and secure password management API",
)

app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=settings.app.cors_origins,
    allow_credentials=True,
    allow_methods=settings.app.cors_methods,
    allow_headers=settings.app.cors_headers,
)

for router in routers:
    app.include_router(router, prefix="/api/v1")


@app.get("/healthcheck", include_in_schema=False)
def healthcheck() -> dict[str, Any]:
    return {"status": "ok"}


@app.get("/hc", include_in_schema=False)
def hc() -> dict[str, Any]:
    return {"status": "ok"}
