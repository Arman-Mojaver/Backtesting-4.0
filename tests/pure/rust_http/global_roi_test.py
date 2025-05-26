import pytest
import requests

from pure.finance_utils.global_roi_test import ROI_RESULT_MAPPING
from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFromDataFactory,
)


@pytest.mark.parametrize(
    ("point_data", "expected_result"),
    list(ROI_RESULT_MAPPING.items()),
)
def test_global_roi(point_data, expected_result, rust_endpoint):
    factory = OperationPointsFromDataFactory(
        mm_strategy_id=1,
        instrument="EURUSD",
        start_date="2024-01-01",
        data=point_data,
    )

    operation_points = factory.operation_points_from_data()

    response = requests.post(
        url=rust_endpoint("global_roi_test"),
        json={"operation_points": operation_points.to_request_format()},
        timeout=5,
    )

    content = parse_response(response)
    assert content["data"] == expected_result
