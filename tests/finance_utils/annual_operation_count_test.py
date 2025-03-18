import pytest

from testing_utils.finance_utils.annual_operation_count import (
    calculate_annual_operation_count,
)
from testing_utils.finance_utils.models import OperationItem


def generate_operations(count: int):
    return [
        OperationItem(
            result=20,
            tp=20,
            sl=20,
            risk=0.02,
        )
        for _ in range(count)
    ]


@pytest.mark.parametrize(
    ("end_date", "operation_items", "expected_result"),
    [
        ("2024-01-01", generate_operations(0), 0.0),
        ("2025-01-01", generate_operations(0), 0.0),
        ("2026-01-01", generate_operations(0), 0.0),
        ("2027-01-01", generate_operations(0), 0.0),
        ("2027-01-01", generate_operations(1), 0.25),
        ("2026-01-01", generate_operations(1), 0.33),
        ("2025-01-01", generate_operations(1), 0.5),
        ("2024-01-01", generate_operations(1), 1.0),
        ("2025-01-01", generate_operations(2), 1.0),
        ("2024-01-01", generate_operations(2), 2.0),
        ("2024-07-01", generate_operations(3), 2.0),
        ("2025-01-01", generate_operations(4), 2.0),
        ("2024-01-01", generate_operations(3), 3.0),
        ("2024-01-01", generate_operations(4), 4.0),
        ("2027-01-01", generate_operations(22), 5.5),
    ],
)
def test_calculate_annual_operation_count(end_date, operation_items, expected_result):
    start_date = "2023-01-01"

    assert (
        calculate_annual_operation_count(
            start_date,
            end_date,
            operation_items,
        )
        == expected_result
    )
