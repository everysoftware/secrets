from typing import Any

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from common.env import Environment


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

    model_config = SettingsConfigDict(env_prefix="postgres_")


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

    model_config = SettingsConfigDict(env_prefix="redis_")


class SMTPSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    from_title: str

    model_config = SettingsConfigDict(env_prefix="smtp_")


class EncryptionSettings(BaseSettings):
    secret: str

    model_config = SettingsConfigDict(env_prefix="encryption_")


class InfrastructureSettings(BaseSettings):
    encryption: EncryptionSettings = EncryptionSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    smtp: SMTPSettings = SMTPSettings()


class CORSSettings(BaseSettings):
    origins: list[str]
    headers: list[str]
    methods: list[str]

    model_config = SettingsConfigDict(env_prefix="cors_")


class AuthSettings(BaseSettings):
    secret: str
    token_lifetime: int

    model_config = SettingsConfigDict(env_prefix="auth_")


class Settings(BaseSettings):
    product_name: str
    version: str = "1"
    environment: Environment

    infrastructure: InfrastructureSettings = InfrastructureSettings()
    auth: AuthSettings = AuthSettings()
    cors: CORSSettings = CORSSettings()

    @property
    def app_config(self) -> dict[str, Any]:
        configs = {"title": f"{self.product_name} API"}

        if self.environment.is_deployed:
            configs["openapi_url"] = None  # скрываем доки

        return configs

    model_config = SettingsConfigDict(env_prefix="", extra="allow")


settings = Settings()
