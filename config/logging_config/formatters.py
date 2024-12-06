import logging

from config import config  # type: ignore[attr-defined]


class EnvFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.environment = config.ENVIRONMENT.upper()
        return super().format(record)
