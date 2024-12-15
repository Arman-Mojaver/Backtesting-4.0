from __future__ import annotations


def simple_moving_average(values: list[int] | list[float], n: int) -> list[float]:
    result_length = len(values) + 1 - n
    return [sum(values[index: index + n]) / n for index in range(result_length)]
