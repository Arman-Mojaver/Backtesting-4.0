from __future__ import annotations

from typing import Any


def set_of_tuples(items: list[Any]) -> set[tuple]:
    return {i.to_tuple() for i in items}
