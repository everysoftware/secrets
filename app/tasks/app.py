from celery import Celery

from app.core.config import cfg

app = Celery("tasks", broker=cfg.redis.dsl, backend=cfg.redis.dsl)
