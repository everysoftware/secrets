from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.api.controllers import routers
from src.infrastructure.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(**settings.app.configs, lifespan=lifespan)
app.add_middleware(
    # TODO: Resolve the issue with the CORS middleware
    CORSMiddleware,
    allow_origins=settings.app.cors_origins,
    allow_credentials=True,
    allow_methods=settings.app.cors_methods,
    allow_headers=settings.app.cors_headers,
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
