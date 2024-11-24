from __future__ import annotations

from typing import Any


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

    for key in dict_1:
        list_1, list_2 = dict_1[key], dict_2[key]

        for item_list_1 in list_1:
            has_equal = False
            for item_list_2 in list_2:
                if item_list_1.to_dict() == item_list_2.to_dict():
                    has_equal = True
                    break

            if not has_equal:
                return False

    return True
