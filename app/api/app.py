import os
from contextlib import asynccontextmanager
from typing import Any, Generator

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.cache.adapter import get_cache
from .routers import routers


@asynccontextmanager
async def lifespan(_: FastAPI) -> Generator[Any, Any, None]:
    cache = await get_cache()
    FastAPICache.init(RedisBackend(cache.client), prefix="fastapi-cache")
    yield


app = FastAPI(title="Secrets", lifespan=lifespan)
current_dir = os.path.dirname(os.path.realpath(__file__))
app.mount("/static", StaticFiles(directory=current_dir + "/static"), name="static")

for router in routers:
    app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/status")
async def status():
    return {"message": "Hello World"}
