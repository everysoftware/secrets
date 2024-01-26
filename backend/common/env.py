import enum
import os
import pathlib

from dotenv import load_dotenv

from .log import log


class Environment(str, enum.Enum):
    LOCAL = "local"
    TESTING = "testing"
    PRODUCTION = "production"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL, self.TESTING)

    @property
    def is_testing(self) -> bool:
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self == self.PRODUCTION


def setup_env() -> None:
    if os.getenv("ENV_LOADED"):
        log.info("Environment variables already loaded, skipping")
        return

    path = pathlib.Path(__file__).parent.parent.parent

    env_files = [".env.dev", ".env"]
    for file in env_files:
        dotenv_path = path.joinpath(file)

        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            log.info(f"Loaded environment variables from {dotenv_path}")
            return

    raise Exception(f"Could not find any of the following files: {env_files}")
