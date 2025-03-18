from __future__ import annotations

from typing import TYPE_CHECKING

from utils.date_utils import string_to_datetime

if TYPE_CHECKING:
    import datetime


def get_difference_in_years(
    date_1: str | datetime.date,
    date_2: str | datetime.date,
) -> float:
    datetime_1 = date_1
    if isinstance(date_1, str):
        datetime_1 = string_to_datetime(date_1)

    datetime_2 = date_2
    if isinstance(date_2, str):
        datetime_2 = string_to_datetime(date_2)

    # Using 365.25 to account for leap years
    return round(abs((datetime_1 - datetime_2).days) / 365.25, 2)
