from __future__ import annotations

from typing import Any


def dicts_by_key_are_equal(dict_1: dict[Any, Any], dict_2: dict[Any, Any]) -> bool:
    if dict_1.keys() != dict_2.keys():
        return False

    return all(dict_1[key].to_dict() == dict_2[key].to_dict() for key in dict_1)
