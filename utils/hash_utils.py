from typing import Any


def make_hashable(value: Any) -> Any:  # noqa: ANN401
    if isinstance(value, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in value.items()))

    if isinstance(value, (list, set)):
        return tuple(make_hashable(v) for v in value)

    return value
