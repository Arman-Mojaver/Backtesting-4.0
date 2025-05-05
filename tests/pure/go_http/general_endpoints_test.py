import requests

from testing_utils.http_utils import parse_response


def test_non_existent_endpoint(go_endpoint):
    response = requests.get(go_endpoint("non_existent_endpoint"), timeout=5)

    assert parse_response(response) == {
        "message": "Server Working. Endpoint not defined!"
    }


def test_ping(go_endpoint):
    response = requests.get(go_endpoint("ping"), timeout=5)

    assert parse_response(response) == {"message": "Ping!"}
