from __future__ import annotations

from typing import Any


def _convert_lists_to_tuples(data: dict[str, Any]):
    if isinstance(data, dict):
        return {key: _convert_lists_to_tuples(value) for key, value in data.items()}

    if isinstance(data, list):
        return tuple(_convert_lists_to_tuples(item) for item in data)

    if isinstance(data, (tuple, set)):
        return type(data)(_convert_lists_to_tuples(item) for item in data)

    return data


def list_of_dicts_are_equal(
    list_1: list[dict[str, Any]],
    list_2: list[dict[str, Any]],
) -> bool:
    converted_list_1 = [_convert_lists_to_tuples(i) for i in list_1]
    converted_list_2 = [_convert_lists_to_tuples(i) for i in list_2]

    return {frozenset(i.items()) for i in converted_list_1} == {
        frozenset(i.items()) for i in converted_list_2
    }
