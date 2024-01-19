from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from domain.config import domain_settings


class CORSSettings(BaseSettings):
    origins: list[str]
    headers: list[str]
    methods: list[str]

    model_config = SettingsConfigDict(env_prefix="cors_")


class AuthSettings(BaseSettings):
    secret: str
    token_lifetime: int

    model_config = SettingsConfigDict(env_prefix="auth_")


class RESTSettings(BaseSettings):
    version: str = "1"

    auth: AuthSettings = AuthSettings()
    cors: CORSSettings = CORSSettings()

    @property
    def app_config(self) -> dict[str, Any]:
        configs = {"title": f"{domain_settings.product_name} API"}

        if domain_settings.environment.is_deployed:
            configs["root_path"] = f"/v{rest_settings.version}"
            configs["openapi_url"] = None  # скрываем доки

        return configs

    model_config = SettingsConfigDict(env_prefix="api_")


rest_settings = RESTSettings()
