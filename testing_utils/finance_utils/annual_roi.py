from __future__ import annotations

from typing import TYPE_CHECKING

from testing_utils.finance_utils.utils import get_difference_in_years

if TYPE_CHECKING:
    import datetime


def calculate_annual_roi(
    start_date: str | datetime.date,
    end_date: str | datetime.date,
    global_roi: float,
) -> float:
    years = get_difference_in_years(start_date, end_date)
    global_accumulated_value = 1 + global_roi / 100
    annual_accumulated_value = global_accumulated_value ** (1 / years)
    return round((annual_accumulated_value - 1) * 100, 2)
