import os
import pathlib
from dataclasses import dataclass
from os import getenv

from arq.connections import RedisSettings
from dotenv import load_dotenv
from sqlalchemy.engine import URL


def setup_env() -> None:
    if os.getenv('TESTING_MODE') is None:
        path = pathlib.Path(__file__).parent.parent
        dotenv_path = path.joinpath('.env' if os.getenv('DOCKER_MODE') is not None else '.dev.env')
        if dotenv_path.exists():
            load_dotenv(dotenv_path)


setup_env()


@dataclass(frozen=True)
class BotConfig:
    tg_token: str = getenv('BOT_TELEGRAM_TOKEN')


@dataclass(frozen=True)
class WebhookConfig:
    on: bool = bool(int(getenv('WEBHOOK_ON', False)))
    ngrok_url: str = getenv('WEBHOOK_URL')
    host: str = getenv('WEBHOOK_HOST', 'localhost')
    port: str = int(getenv('WEBHOOK_PORT', 8080))
    path: str = f'/bot/{BotConfig.tg_token}'
    url: str = f'{ngrok_url}{path}'


@dataclass(frozen=True)
class DatabaseConfig:
    db: str = getenv('POSTGRES_DB', 'postgres')
    username: str = getenv('POSTGRES_USER', 'postgres')
    password: str = getenv('POSTGRES_PASSWORD', None)

    port: int = int(getenv('POSTGRES_PORT', 5432))
    host: str = getenv('POSTGRES_HOST', 'postgres')

    driver: str = 'asyncpg'
    database_system: str = 'postgresql'

    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.username,
            database=self.db,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass(frozen=True)
class RedisConfig:
    db: str = getenv('REDIS_DATABASE', 1)
    username: str = getenv('REDIS_USERNAME', None)
    password: str = getenv('REDIS_PASSWORD', None)
    port: int = int(getenv('REDIS_PORT', 6379))
    host: str = getenv('REDIS_HOST', 'redis')

    state_ttl: int = getenv('REDIS_TTL_STATE', None)
    data_ttl: int = getenv('REDIS_TTL_DATA', None)

    pool_settings = RedisSettings(
        username=username,
        password=password,
        port=port,
        host=host
    )


@dataclass(frozen=True)
class Config:
    mode: str = getenv('BOT_MODE', 'dev')
    debug: bool = bool(getenv('BOT_DEBUG'))
    logging_level: int = getenv('BOT_LOGGING_LEVEL', 'INFO')

    bot: BotConfig = BotConfig()
    webhook: WebhookConfig = WebhookConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()


cfg = Config()
