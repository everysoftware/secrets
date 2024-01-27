from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from common.settings import settings
from infrastructure.redis import redis, pool
from interfaces.controllers import routers


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    await redis.ping()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield

    await pool.disconnect()


app = FastAPI(**settings.app_config, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=settings.cors.methods,
    allow_headers=settings.cors.headers,
)

add_pagination(app)


@app.exception_handler(HTTPException)
async def http_exception_handler(_app, exc) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/ping", include_in_schema=False)
async def ping():
    return {"message": "pong"}


for router in routers:
    app.include_router(router)
