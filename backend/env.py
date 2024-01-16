import pathlib

from dotenv import load_dotenv


def setup_env() -> None:
    path = pathlib.Path(__file__).parent.parent

    env_files = [".env.dev", ".env"]
    for file in env_files:
        dotenv_path = path.joinpath(file)

        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            print(f"Loaded environment variables from {dotenv_path}")
            break
