from typing import Any, Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy import URL


class DatabaseSettings(BaseSettings):
    driver_name: str = "postgresql+asyncpg"
    host: str
    port: int
    db: str
    user: str
    password: str

    @property
    def dsn(self) -> PostgresDsn:
        return URL.create(
            drivername=self.driver_name,
            database=self.db,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ).render_as_string(hide_password=False)

    model_config = SettingsConfigDict(extra="allow", env_prefix="postgres_")


class RedisSettings(BaseSettings):
    host: str
    port: int
    database: int
    username: str
    password: str

    ttl_state: int | None = None
    ttl_data: int | None = None

    @property
    def dsn(self) -> RedisDsn:
        return f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = SettingsConfigDict(extra="allow", env_prefix="redis_")


class SMTPSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    from_title: str

    model_config = SettingsConfigDict(extra="allow", env_prefix="smtp_")


class AppSettings(BaseSettings):
    product: str = "Test"
    version: str = "1"

    auth_secret: str
    auth_second_secret: str
    auth_token_lifetime: int
    auth_second_token_lifetime: int
    auth_algorithm: Literal["HS256", "HS512", "RS256", "RS512"] = "HS256"

    cors_origins: list[str]
    cors_headers: list[str]
    cors_methods: list[str]

    encryption_secret: str

    @property
    def configs(self) -> dict[str, Any]:
        configs = {"title": f"{self.product} API"}

        return configs

    model_config = SettingsConfigDict(extra="allow", env_prefix="")


class Settings:
    db: DatabaseSettings
    redis: RedisSettings
    smtp: SMTPSettings
    app: AppSettings

    def __init__(self) -> None:
        self.db = DatabaseSettings()
        self.redis = RedisSettings()
        self.smtp = SMTPSettings()
        self.app = AppSettings()
