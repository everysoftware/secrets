from pydantic_settings import BaseSettings, SettingsConfigDict

from secrets_app.skeleton.settings import Postgres, API, load_env, ConnectionUrl


class PgSettings(BaseSettings, Postgres):
    model_config = SettingsConfigDict(extra="allow", env_prefix="postgres_")


class SMTPSettings(BaseSettings, ConnectionUrl):
    from_user: str

    model_config = SettingsConfigDict(extra="allow", env_prefix="smtp_")


class AppSettings(BaseSettings, API):
    auth_secret: str
    auth_token_lifetime: int

    encryption_secret: str

    model_config = SettingsConfigDict(extra="allow", env_prefix="app_")


class Settings:
    db: PgSettings
    smtp: SMTPSettings
    app: AppSettings

    def __init__(self) -> None:
        self.db = PgSettings()
        self.smtp = SMTPSettings()
        self.app = AppSettings()


def get_settings() -> Settings:
    load_env()
    settings_ = Settings()
    return settings_


settings = get_settings()
