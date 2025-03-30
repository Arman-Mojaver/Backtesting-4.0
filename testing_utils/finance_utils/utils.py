from __future__ import annotations

from typing import TYPE_CHECKING, Any

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


def zigzag_split(list_of_items: list[Any], count: int) -> tuple[list[Any], list[Any]]:
    indices = [int(i * len(list_of_items) / count) for i in range(count)]
    items = [list_of_items[i] for i in indices]

    list_1, list_2 = [], []
    for index, elem in enumerate(items):
        if index % 2 == 0:
            list_1.append(elem)
        else:
            list_2.append(elem)

    return list_1, list_2


def get_lists_evenly_spaced_samples(
    list_of_items: list[Any],
    long_count: int,
    short_count: int,
) -> tuple[list[Any], list[Any]]:
    if not list_of_items or long_count < 0 or short_count < 0:
        err = f"Invalid inputs: {list_of_items=}, {long_count=}, {short_count=}"
        raise ValueError(err)

    if not (long_count or short_count):
        err = "Both counts can not be 0"
        raise ValueError(err)

    if abs(long_count - short_count) > 1:
        err = (
            "Absolute difference between counts can not be greater than 1: "
            f"{long_count=}, {short_count=}"
        )
        raise ValueError(err)

    total_count = long_count + short_count
    if total_count > len(list_of_items):
        err = (
            "Total count can not be greater than list of items: "
            f"{list_of_items=}, {total_count=}"
        )
        raise ValueError(err)

    big_list, small_list = zigzag_split(list_of_items, total_count)

    if long_count >= short_count:
        return big_list, small_list

    return small_list, big_list
