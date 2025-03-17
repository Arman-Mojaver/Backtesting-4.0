from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint
    from testing_utils.finance_utils.models import OperationItem


def calculate_global_roi(
    operation_items: list[OperationItem] | list[LongOperationPoint | ShortOperationPoint],
) -> float:
    cumsum = 1
    for item in operation_items:
        result = item.result * (item.risk / item.sl)
        cumsum += result

    return round((cumsum - 1) * 100, 2)
