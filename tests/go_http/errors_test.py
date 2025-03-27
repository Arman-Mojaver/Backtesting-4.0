from http import HTTPStatus

import pytest
import requests

from testing_utils.http_utils import parse_response


def test_non_existent_endpoint(endpoint):
    response = requests.get(endpoint("non_existent_endpoint"), timeout=5)

    assert parse_response(response) == {
        "message": "Server Working. Endpoint not defined!"
    }


def test_ping(endpoint):
    response = requests.get(endpoint("ping"), timeout=5)

    assert parse_response(response) == {"message": "Ping!"}


@pytest.mark.parametrize("http_method", ["GET", "PUT", "DELETE"])
def test_process_only_accepts_post_requests(http_method, endpoint):
    response = requests.request(
        method=http_method,
        url=endpoint("process_strategies"),
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
def test_process_invalid_json(invalid_body, endpoint):
    response = requests.post(
        url=endpoint("process_strategies"),
        json=invalid_body,
        timeout=5,
    )

    assert parse_response(response) == {"error": "Invalid JSON"}
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_process_valid_fields(endpoint):
    response = requests.post(url=endpoint("process_strategies"), json={}, timeout=5)

    assert response.status_code == HTTPStatus.OK
