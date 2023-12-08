import os
import pathlib
from dataclasses import dataclass
from os import getenv

from arq.connections import RedisSettings
from dotenv import load_dotenv
from sqlalchemy.engine import URL


def setup_env() -> None:
    if os.getenv("TESTING_MODE") is None and os.getenv("DOCKER_MODE") is None:
        path = pathlib.Path(__file__).parent.parent.parent
        dotenv_path = path.joinpath(".dev.env")
        if dotenv_path.exists():
            load_dotenv(dotenv_path)


setup_env()


@dataclass(frozen=True)
class BotConfig:
    tg_token: str = getenv("BOT_TELEGRAM_TOKEN", "FILL ME")


@dataclass(frozen=True)
class WebhookConfig:
    on: bool = bool(int(getenv("WEBHOOK_ON", "0")))
    ngrok_url: str = getenv("WEBHOOK_URL", "FILL ME")
    host: str = getenv("WEBHOOK_HOST", "localhost")
    port: int = int(getenv("WEBHOOK_PORT", 8080))
    path: str = f"app/bot/{BotConfig.tg_token}"
    url: str = f"{ngrok_url}{path}"


@dataclass(frozen=True)
class DatabaseConfig:
    db: str = getenv("POSTGRES_DB", "postgres")
    username: str = getenv("POSTGRES_USER", "postgres")
    password: str = getenv("POSTGRES_PASSWORD", "postgres")
    port: int = int(getenv("POSTGRES_PORT", 5432))
    host: str = getenv("POSTGRES_HOST", "")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    dsl: str = URL.create(
        drivername=f"{database_system}+{driver}",
        username=username,
        database=db,
        password=password,
        port=port,
        host=host,
    ).render_as_string(hide_password=False)


@dataclass(frozen=True)
class RedisConfig:
    db: int = int(getenv("REDIS_DATABASE", "1"))
    username: str = getenv("REDIS_USERNAME", "redis")
    password: str | None = getenv("REDIS_PASSWORD")
    port: int = int(getenv("REDIS_PORT", "6379"))
    host: str = getenv("REDIS_HOST", "redis")

    state_ttl: int = int(getenv("REDIS_TTL_STATE", str(24 * 60 * 60)))
    data_ttl: int = int(getenv("REDIS_TTL_DATA", str(24 * 60 * 60)))

    pool_settings = RedisSettings(
        username=username, password=password, port=port, host=host
    )

    dsl: str = f"redis://{username}:{password}@{host}:{port}"


@dataclass(frozen=True)
class APIConfig:
    host: str = getenv("API_HOST", "localhost")
    port: int = int(getenv("API_PORT", "8000"))
    url: str = f"{host}:{port}"
    secret_auth: str = getenv("API_SECRET_AUTH", "FILL ME")
    secret_encryption: str = getenv("API_SECRET_ENCRYPTION", "FILL ME")


@dataclass(frozen=True)
class SMTPConfig:
    host: str = getenv("SMTP_HOST", "smtp.gmail.com")
    port: int = int(getenv("SMTP_PORT", "465"))
    username: str = getenv("SMTP_USERNAME", "FILL ME")
    password: str = getenv("SMTP_PASSWORD", "FILL ME")
    sender: str = getenv("SMTP_FROM", "Secrets")


@dataclass(frozen=True)
class Config:
    mode: str = getenv("BOT_MODE", "docker")
    debug: bool = bool(int(getenv("BOT_DEBUG", "0")))
    logging_level: str = getenv("BOT_LOGGING_LEVEL", "INFO")

    bot: BotConfig = BotConfig()
    webhook: WebhookConfig = WebhookConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    api: APIConfig = APIConfig()
    smtp: SMTPConfig = SMTPConfig()


cfg = Config()
