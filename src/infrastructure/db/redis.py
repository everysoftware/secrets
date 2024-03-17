from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from src.infrastructure.config import settings

pool = ConnectionPool.from_url(
    settings.redis.dsn, max_connections=10, decode_responses=True
)
redis = Redis(connection_pool=pool)
