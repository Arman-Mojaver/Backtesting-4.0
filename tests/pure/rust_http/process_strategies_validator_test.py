import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)
from testing_utils.request_body_factory.indicator_factory import (
    generate_macd_indicators,
    generate_rsi_indicators,
)


@pytest.mark.parametrize(
    (
        "money_management_strategy_id",
        "long_operation_points",
        "short_operation_points",
        "indicators",
    ),
    [
        # Empty inputs
        (
            1,
            [],
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
            [*generate_rsi_indicators(2)],
        ),
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-01", 10),
            [],
            [*generate_rsi_indicators(2)],
        ),
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-01", 10),
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
            [],
        ),
        # instrument mismatch
        (
            1,
            generate_random_long_operation_points(1, "USDCAD", "2024-01-01", 1)
            + generate_random_long_operation_points(1, "EURUSD", "2024-01-02", 9),
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
            [*generate_rsi_indicators(2)],
        ),
        # date mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-10", 10),
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
            [*generate_rsi_indicators(2)],
        ),
        # money management strategy mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-01", 1)
            + generate_random_long_operation_points(2, "EURUSD", "2024-01-02", 9),
            generate_random_short_operation_points(2, "EURUSD", "2024-01-01", 10),
            [*generate_rsi_indicators(2)],
        ),
        # indicator type mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-01", 10),
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
            [*generate_rsi_indicators(2), *generate_macd_indicators(2)],
        ),
    ],
)
def test_process_strategies_validator_returns_error(
    money_management_strategy_id,
    long_operation_points,
    short_operation_points,
    indicators,
    rust_endpoint,
):
    data = {
        "money_management_strategy_id": money_management_strategy_id,
        "long_operation_points": [p.to_request_format() for p in long_operation_points],
        "short_operation_points": [p.to_request_format() for p in short_operation_points],
        "indicators": [i.to_request_format() for i in indicators],
    }

    response = requests.post(
        url=rust_endpoint("process_strategies_validator"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content == {"error": "process_strategies_validator"}


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
        "indicators": [i.to_request_format() for i in generate_rsi_indicators(2)],
    }

    response = requests.post(
        url=rust_endpoint("process_strategies_validator"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content.get("data") == "OK!"
