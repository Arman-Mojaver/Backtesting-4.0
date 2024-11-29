from __future__ import annotations

from typing import Any


def list_items_are_equal(list_: list[Any]) -> bool:
    return all(item == list_[0] for item in list_)
