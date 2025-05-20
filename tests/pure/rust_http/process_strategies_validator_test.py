import requests

from testing_utils.http_utils import parse_response
from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)


def test_success(rust_endpoint):
    money_management_strategy_id = 1
    long_operation_points = generate_random_long_operation_points(
        money_management_strategy_id,
        "EURUSD",
        "2024-01-01",
        10,
    )

    short_operation_points = generate_random_short_operation_points(
        money_management_strategy_id,
        "EURUSD",
        "2024-01-01",
        10,
    )

    data = {
        "money_management_strategy_id": money_management_strategy_id,
        "long_operation_points": [p.to_request_format() for p in long_operation_points],
        "short_operation_points": [p.to_request_format() for p in short_operation_points],
    }

    response = requests.post(
        url=rust_endpoint("process_strategies_validator"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content["data"] == "OK!"
