from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint
    from testing_utils.finance_utils.models import OperationItem


def calculate_max_draw_down(
    operation_items: list[OperationItem] | list[LongOperationPoint | ShortOperationPoint],
) -> float:
    cumsum, cummax = 1, 1
    draw_downs = []
    for item in operation_items:
        result = item.result * (item.risk / item.sl)
        cumsum += result
        cummax = max(cummax, cumsum)
        draw_down = (cummax - cumsum) / cummax
        rounded_draw_down = round(draw_down * 100, 2)

        draw_downs.append(rounded_draw_down)

    return max(draw_downs)
