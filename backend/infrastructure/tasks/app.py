from celery import Celery

from infrastructure.config import infrastructure_settings

app = Celery(
    main="tasks",
    broker=infrastructure_settings.redis.dsn,
    backend=infrastructure_settings.redis.dsn,
)
