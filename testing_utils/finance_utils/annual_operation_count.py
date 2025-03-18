from __future__ import annotations

from typing import TYPE_CHECKING

from testing_utils.finance_utils.utils import get_difference_in_years

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint
    from testing_utils.finance_utils.models import OperationItem


def calculate_annual_operation_count(
    start_date: str,
    end_date: str,
    operation_items: list[OperationItem] | list[LongOperationPoint | ShortOperationPoint],
) -> float:
    years = get_difference_in_years(start_date, end_date)
    return round(len(operation_items) / years, 2)
