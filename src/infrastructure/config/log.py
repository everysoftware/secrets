from __future__ import annotations

import os

import loguru
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerSettings(BaseSettings):
    path: str = "logs"
    stdout_filename: str = "stdout.log"
    stderr_filename: str = "stderr.log"
    rotation: str = "10 MB"
    retention: str = "15 days"
    compression: str = "tar.gz"

    @field_validator("path")
    def validate_log_config(cls, v: str) -> str:
        if not os.path.exists(v):
            raise ValueError(f"Log path {v} does not exist")
        return v

    model_config = SettingsConfigDict(env_prefix="log_")


logger_settings = LoggerSettings()

log_config = {
    "rotation": logger_settings.rotation,
    "retention": logger_settings.retention,
    "compression": logger_settings.compression,
    # Логи добавляются в очередь перед записью, чтобы избежать блокировки ввода-вывода.
    "enqueue": True,
}


def stdout_filter(record: loguru.Record) -> bool:
    level: loguru.RecordLevel = record["level"]
    return level.name == "INFO" or level.no <= 25


def stderr_filter(record: loguru.Record) -> bool:
    level: loguru.RecordLevel = record["level"]
    return level.name == "ERROR" or level.no >= 30


def setup_stdout() -> None:
    log_file = os.path.join(logger_settings.path, logger_settings.stdout_filename)
    loguru.logger.add(
        log_file,
        level="INFO",
        filter=stdout_filter,
        **log_config,
        backtrace=False,
        diagnose=False,
    )


def setup_stderr() -> None:
    log_file = os.path.join(logger_settings.path, logger_settings.stderr_filename)
    loguru.logger.add(
        log_file,
        level="ERROR",
        filter=stderr_filter,
        **log_config,
        backtrace=True,
        diagnose=True,
    )


setup_stdout()
setup_stderr()

log = loguru.logger
