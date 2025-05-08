import pytest

from testing_utils.finance_utils.annual_roi import calculate_annual_roi

END_DATE_GLOBAL_ROI = [
    ("2024-01-01", 10),  # 1 year
    ("2025-01-01", 21.0),  # 2 years. round(((1.1 * 1.1) - 1) * 100, 2)
    ("2026-01-01", 33.1),  # 3 years. round(((1.1 * 1.1 * 1.1) - 1) * 100, 2)
    ("2027-01-01", 46.41),  # 4 years. round(((1.1 * 1.1 * 1.1 * 1.1) - 1) * 100, 2)
    (
        "2028-01-01",
        61.05,
    ),  # 5 years. round(((1.1 * 1.1 * 1.1 * 1.1 * 1.1) - 1) * 100, 2)
    ("2023-07-01", 4.88),  # 0.5 years. round(((1.1 ** 0.5) - 1) * 100, 2)
    ("2024-07-01", 15.37),  # 1.5 years. round(((1.1 * 1.1 ** 0.5) - 1) * 100, 2)
    ("2023-04-01", 2.411),  # 0.25 years. round(((1.1**0.25) - 1) * 100, 3)
    ("2023-05-01", 3.195),  # 0.33 years. round(((1.1**0.33) - 1) * 100, 3)
]


@pytest.mark.parametrize(("end_date", "global_roi"), END_DATE_GLOBAL_ROI)
def test_calculate_annual_roi(end_date, global_roi):
    start_date, expected_result = "2023-01-01", 10.0
    assert calculate_annual_roi(start_date, end_date, global_roi) == expected_result
