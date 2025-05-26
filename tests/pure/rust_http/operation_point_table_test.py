import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFactory,
)


@pytest.mark.parametrize(
    "end_date", ["2024-01-01", "2024-01-02", "2024-02-01", "2025-01-01"]
)
@pytest.mark.parametrize(
    "operation_points_type", ["long_operation_points", "short_operation_points"]
)
def test_long_operation_points_table(end_date, operation_points_type, rust_endpoint):
    start_date = "2024-01-01"
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=1,
        start_date=start_date,
        end_date=end_date,
    )

    operation_points = getattr(operation_points_factory, operation_points_type)
    data = {"operation_points": operation_points.to_request_format()}

    response = requests.post(
        url=rust_endpoint("operation_points_table_test"),
        json=data,
        timeout=5,
    )

    expected_result = [
        [item["timestamp"], item] for item in operation_points.to_request_format()
    ]

    content = parse_response(response)
    assert content["data"] == expected_result
