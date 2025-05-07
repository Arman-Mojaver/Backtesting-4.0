from http import HTTPStatus

import pytest
import requests

from testing_utils.http_utils import parse_response

ENDPOINT_PATHS = (
    "process_strategies",
    "rsi",
    # Tests
    "annual_operation_count",
    "max_draw_down",
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
        (1, 2, 3),
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
