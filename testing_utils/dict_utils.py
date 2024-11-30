from __future__ import annotations

from typing import Any


def lists_are_equal(list_1: list[Any], list_2: list[Any]) -> bool:
    return all(
        any(item1.to_dict() == item2.to_dict() for item2 in list_2) for item1 in list_1
    )


def dicts_by_key_are_equal(dict_1: dict[Any, Any], dict_2: dict[Any, Any]) -> bool:
    if dict_1.keys() != dict_2.keys():
        return False

    return all(dict_1[key].to_dict() == dict_2[key].to_dict() for key in dict_1)


def dicts_multi_by_key_are_equal(
    dict_1: dict[str, list[Any]],
    dict_2: dict[str, list[Any]],
) -> bool:
    if dict_1.keys() != dict_2.keys():
        return False

    return all(lists_are_equal(dict_1[key], dict_2[key]) for key in dict_1)


def list_of_dicts_are_equal(
    list_1: list[dict[str, Any]],
    list_2: list[dict[str, Any]],
) -> bool:
    return {frozenset(i.items()) for i in list_1} == {
        frozenset(i.items()) for i in list_2
    }
