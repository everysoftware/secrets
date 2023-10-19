import asyncio
from typing import Any, Optional, TypeVar

from redis.asyncio.client import Redis

from src.config import cfg

KeyLike = TypeVar("KeyLike", str, int)


def build_redis_client() -> Redis:
    client = Redis(
        host=cfg.redis.host,
        db=cfg.redis.db,
        port=cfg.redis.port,
        password=cfg.redis.password,
        username=cfg.redis.username,
    )

    asyncio.create_task(client.ping())

    return client


class Cache:
    client: Redis

    def __init__(self, redis: Optional[Redis] = None):
        self.client = redis or build_redis_client()

    @property
    def redis_client(self) -> Redis:
        return self.client

    async def get(self, key: KeyLike) -> Any:
        return await self.client.get(str(key))

    async def set(self, key: KeyLike, value: Any):
        await self.client.set(name=str(key), value=value)
