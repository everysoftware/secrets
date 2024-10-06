from typing import Literal

from app.auth.config import AuthSettings
from app.db.config import DBSettings
from app.security.config import SecuritySettings
from app.schemas import SettingsBase


class CORSSettings(SettingsBase):
    cors_headers: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_origins: list[str] = ["*"]
    cors_origin_regex: str | None = None


class Settings(SettingsBase):
    app_name: str = "fastapiapp"
    app_display_name: str = "FastAPI App"
    app_version: str = "0.1.0"
    app_env: Literal["dev", "prod"] = "dev"
    app_debug: bool = False
    app_domain: str = "localhost:8000"
    app_root_path: str = "/api/v1"

    app: AuthSettings = AuthSettings()
    security: SecuritySettings = SecuritySettings()
    cors: CORSSettings = CORSSettings()
    db: DBSettings = DBSettings()


settings = Settings()
