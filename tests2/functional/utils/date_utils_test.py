from datetime import datetime, timezone

import pytest

from config import config  # type: ignore[attr-defined]
from utils.date_utils import DateError, datetime_to_string, string_to_datetime

args__expected_result__datetime_from_string_is_valid = [
    (("2023-01-05",), datetime(year=2023, month=1, day=5, tzinfo=timezone.utc)),
    (
        ("2023-01-05", config.DATE_FORMAT),
        datetime(year=2023, month=1, day=5, tzinfo=timezone.utc),
    ),
    (
        ("2023-01-05 05:45:00", config.DATETIME_FORMAT),
        datetime(year=2023, month=1, day=5, hour=5, minute=45, tzinfo=timezone.utc),
    ),
]


@pytest.mark.parametrize(
    ("args", "expected_result"),
    args__expected_result__datetime_from_string_is_valid,
    ids=str,
)
def test_string_to_datetime_is_valid(args, expected_result):
    assert string_to_datetime(*args) == expected_result


args__is_invalid__string_to_datetime_is_invalid = [
    ("random_string",),
    ("random_string", config.DATE_FORMAT),
    ("random_string", config.DATETIME_FORMAT),
    ("01-05-2023",),
    ("01-05-2023", config.DATE_FORMAT),
    ("01-05-2023", config.DATETIME_FORMAT),
    ("01-05-2023 01:30",),
    ("01-05-2023 01:30", config.DATE_FORMAT),
    ("01-05-2023 01:30", config.DATETIME_FORMAT),
]


@pytest.mark.parametrize(
    "args",
    args__is_invalid__string_to_datetime_is_invalid,
    ids=str,
)
def test_string_to_datetime_is_invalid(args):
    with pytest.raises(DateError):
        string_to_datetime(*args)


args__expected_result__datetime_to_string_is_valid = [
    (
        (datetime(year=2023, month=1, day=5, hour=5, minute=45, tzinfo=timezone.utc),),
        "2023-01-05",
    ),
    (
        (
            datetime(year=2023, month=1, day=5, hour=5, minute=45, tzinfo=timezone.utc),
            config.DATE_FORMAT,
        ),
        "2023-01-05",
    ),
    (
        (
            datetime(year=2023, month=1, day=5, hour=5, minute=45, tzinfo=timezone.utc),
            config.DATETIME_FORMAT,
        ),
        "2023-01-05 05:45:00",
    ),
]


@pytest.mark.parametrize(
    ("args", "expected_result"),
    args__expected_result__datetime_to_string_is_valid,
    ids=str,
)
def test_datetime_to_string_is_valid(args, expected_result):
    assert datetime_to_string(*args) == expected_result


args__is_invalid__datetime_to_string_is_invalid = [
    ("random_string",),
    (123456,),
    ([2023, 1, 5],),
    ({"year": 2023, "month": 1, "day": 5},),
]


@pytest.mark.parametrize(
    "args",
    args__is_invalid__datetime_to_string_is_invalid,
    ids=str,
)
def test_datetime_to_string_is_invalid(args):
    with pytest.raises(DateError):
        datetime_to_string(*args)
