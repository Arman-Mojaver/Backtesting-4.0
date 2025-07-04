from http import HTTPStatus

import pytest
import requests

from testing_utils.http_utils import parse_response

ENDPOINT_PATHS = (
    "process_strategies",
    # Tests
    "process_strategies_test",
    "annual_operation_count_test",
    "annual_roi_from_global_roi_test",
    "global_roi_test",
    "max_draw_down_test",
    "operation_points_table_test",
    "operation_points_filter_test",
    "process_strategies_validator_test",
    "process_strategies_from_signals_test",
    "process_strategy_test",
    "query_long_operation_points_by_mms_test",
    "query_short_operation_points_by_mms_test",
    "query_resampled_points_by_instrument_test",
    "query_indicators_by_type_test",
    "strategy_profitability_test",
    "oscillator_test",
    "crossover_test",
    "thresholds_test",
    "commit_strategy_groups_test",
    # Indicators
    "rsi_test",
)


@pytest.fixture(params=ENDPOINT_PATHS)
def endpoint_path(request):
    return request.param


@pytest.mark.parametrize("http_method", ["GET", "PUT", "DELETE"])
def test_only_accepts_post_requests(http_method, rust_endpoint, endpoint_path):
    response = requests.request(
        method=http_method,
        url=rust_endpoint(endpoint_path),
        timeout=5,
    )

    assert parse_response(response) == {"error": "Method Not Allowed"}
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "invalid_body",
    [
        1,
        1.5,
        "random_string",
        (1, 2, 3, 4),
    ],
)
def test_invalid_json(invalid_body, rust_endpoint, endpoint_path):
    response = requests.post(
        url=rust_endpoint(endpoint_path),
        json=invalid_body,
        timeout=5,
    )

    assert parse_response(response) == {"error": "Invalid JSON"}
    assert response.status_code == HTTPStatus.BAD_REQUEST
