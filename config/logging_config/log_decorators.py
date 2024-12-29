import logging
from collections.abc import Callable
from logging import INFO

from logdecorator import log_on_end as log_on_end_
from logdecorator import log_on_start as log_on_start_

from logger import log


def log_on_start(message: str, logger: logging.Logger = log) -> Callable:
    return log_on_start_(
        message=message,
        logger=logger,
        log_level=INFO,
    )


def log_on_end(message: str, logger: logging.Logger = log) -> Callable:
    return log_on_end_(
        message=message,
        logger=logger,
        log_level=INFO,
    )
