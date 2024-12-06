from __future__ import annotations

from datetime import date, datetime, timezone

from config import config  # type: ignore[attr-defined]


class DateError(Exception):
    pass


def string_to_datetime(
    string: str,
    format: str = config.DATE_FORMAT,  # noqa: A002
) -> datetime:
    try:
        return datetime.strptime(string, format).replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise DateError from e


def datetime_to_string(
    date: datetime | date,
    format: str = config.DATE_FORMAT,  # noqa: A002
) -> str:
    try:
        return datetime.strftime(date, format)
    except ValueError as e:
        raise DateError from e
