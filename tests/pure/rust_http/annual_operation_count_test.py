from __future__ import annotations

import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFactory,
)
from utils.date_utils import string_to_datetime


@pytest.mark.parametrize(
    ("end_date", "count", "expected_result"),
    [
        # 1 Year
        ("2025-01-01", 0, 0.0),
        ("2025-01-01", 1, 1.0),
        ("2025-01-01", 2, 2.0),
        ("2025-01-01", 3, 3.0),
        ("2025-01-01", 4, 4.0),
        ("2025-01-01", 100, 100.0),
        # 2 Years
        ("2026-01-01", 0, 0.0),
        ("2026-01-01", 1, 0.5),
        ("2026-01-01", 2, 1.0),
        ("2026-01-01", 3, 1.5),
        ("2026-01-01", 4, 2.0),
        ("2026-01-01", 5, 2.5),
        ("2026-01-01", 300, 150),
    ],
)
def test_annual_operation_count(end_date, count, expected_result, rust_endpoint):
    start_date = "2024-01-01"
    factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=1,
        start_date=start_date,
        end_date=end_date,
    )

    operation_points = factory.get_evenly_spaced(count=count)
    data = {
        "operation_points": operation_points.to_request_format(),
        "start_date": int(string_to_datetime(start_date).timestamp()),
        "end_date": int(string_to_datetime(end_date).timestamp()),
    }

    response = requests.post(
        url=rust_endpoint("annual_operation_count"),
        json=data,
        timeout=5,
    )
    content = parse_response(response)
    # TODO: Fix or reduce rounding error  # noqa: FIX002, TD002, TD003
    assert abs(content["data"] - expected_result) <= 0.3
