from __future__ import annotations


def get_sma(values: list[int] | list[float], n: int) -> list[float]:
    """Simple Moving Average."""  # noqa: D401
    result_length = len(values) + 1 - n
    return [sum(values[index : index + n]) / n for index in range(result_length)]
