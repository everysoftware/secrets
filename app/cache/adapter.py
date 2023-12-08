import asyncio
from typing import Any

from redis.asyncio.client import Redis

from app.core.config import cfg


def build_redis_client() -> Redis:
    client = Redis(
        host=cfg.redis.host,
        db=cfg.redis.db,
        port=cfg.redis.port,
        password=cfg.redis.password,
    )

    return client


class Cache:
    client: Redis

    def __init__(self, redis: Redis | None = None):
        self.client = redis or build_redis_client()

    async def get(self, key: str, type_: Any = None) -> Any:
        result = await self.client.get(key)

        if result is None:
            return result

        return type_(result) if type_ is not None else result

    async def set(self, key: str, value: Any):
        return await self.client.set(name=key, value=value)

    async def delete(self, key: str):
        return await self.client.delete(key)

    async def on_startup(self) -> None:
        asyncio.create_task(self.client.ping())


async def get_cache() -> Cache:
    return Cache()
