from __future__ import annotations

from typing import TYPE_CHECKING

from indicators.sma import get_sma

if TYPE_CHECKING:
    from database.models import ResampledPointD1


def get_true_range(resampled_points: list[ResampledPointD1]) -> list[float]:
    true_range_values = [resampled_points[0].high - resampled_points[0].low]

    for index, point in enumerate(resampled_points[1:], 1):
        previous_point = resampled_points[index - 1]
        true_range = max(
            point.high - point.low,
            abs(point.high - previous_point.close),
            abs(point.low - previous_point.close),
        )
        true_range_values.append(true_range)

    return true_range_values


def get_atr(true_range_values: list[float], atr_parameter: int) -> list[float]:
    """Average True Range."""
    return get_sma(true_range_values, atr_parameter)
