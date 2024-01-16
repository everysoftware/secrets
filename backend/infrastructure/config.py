from pydantic import RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
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


class InfrastructureSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    smtp: SMTPSettings = SMTPSettings()


infrastructure_settings = InfrastructureSettings()
