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
