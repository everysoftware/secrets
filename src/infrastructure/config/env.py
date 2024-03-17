import pathlib

from dotenv import load_dotenv

from .log import log
from .settings import Settings


def get_settings() -> Settings:
    log.info("Loading settings...")
    path = pathlib.Path(__file__).parent.parent.parent.parent

    env_files = [path.joinpath(file) for file in (".env.dev", ".env")]

    for file in env_files:
        if file.exists():
            log.info(f"Using {file}...")
            load_dotenv(file)
            log.info("Settings loaded")

            return Settings()

    raise ValueError(f"No setting files: {env_files}")


settings = get_settings()
