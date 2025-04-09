from __future__ import annotations

from collections import defaultdict
from typing import Any


def dict_multi_by_key(items: list[Any], key: str) -> dict[str, list[Any]]:
    dictionary = defaultdict(list)
    for item in items:
        dict_key = getattr(item, key, None)
        if not dict_key:
            continue

        dictionary[dict_key].append(item)

    return dictionary


def dict_by_key(items: list[Any], key: Any) -> dict[Any, Any]:  # noqa: ANN401
    multiple_items_by_key = dict_multi_by_key(items, key)

    for k, v in multiple_items_by_key.items():
        if len(v) != 1:
            err = f"Multiple items found with key '{k}'.."
            raise ValueError(err)

    return {k: v[0] for k, v in multiple_items_by_key.items()}
