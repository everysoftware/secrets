from typing import Literal

from pydantic_settings import SettingsConfigDict

from app.db.config import DBSettings
from app.schemas import SettingsBase


class AppSettings(SettingsBase):
    title: str = "Secrets API"
    version: str = "0.1.0"
    env: Literal["dev", "prod"] = "dev"
    cors_headers: list[str] = ["*"]
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    auth_secret: str = "changethis"
    auth_token_lifetime: int = 3600
    encryption_secret: str = "changethis"

    model_config = SettingsConfigDict(env_prefix="app_")


class Settings:
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()


settings = Settings()
