from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from common.settings import settings

pool = ConnectionPool.from_url(
    settings.infrastructure.redis.dsn, max_connections=10, decode_responses=True
)
redis = Redis(connection_pool=pool)
