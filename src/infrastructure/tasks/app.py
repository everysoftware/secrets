from celery import Celery

from common.settings import settings

app = Celery(
    main="tasks",
    broker=settings.infrastructure.redis.dsn,
    backend=settings.infrastructure.redis.dsn,
)
