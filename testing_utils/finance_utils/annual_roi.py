from testing_utils.finance_utils.utils import get_difference_in_years


def calculate_annual_roi(start_date: str, end_date: str, global_roi: float) -> float:
    years = get_difference_in_years(start_date, end_date)
    global_accumulated_value = 1 + global_roi / 100
    annual_accumulated_value = global_accumulated_value ** (1 / years)
    return round((annual_accumulated_value - 1) * 100, 2)
