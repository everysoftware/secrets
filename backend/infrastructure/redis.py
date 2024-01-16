from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from infrastructure.config import infrastructure_settings

pool = ConnectionPool.from_url(
    infrastructure_settings.redis.dsn, max_connections=10, decode_responses=True
)
redis = Redis(connection_pool=pool)
