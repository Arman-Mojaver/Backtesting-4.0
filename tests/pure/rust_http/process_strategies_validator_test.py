from __future__ import annotations

import pytest
import requests

from database.models import ResampledPointD1
from fixtures.price_data import get_resampled_d1_data
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
from utils.date_utils import string_to_datetime


def generate_resampled_points(resampled_point_data) -> list[ResampledPointD1]:
    resampled_points = [ResampledPointD1(**item) for item in resampled_point_data]
    for index, p in enumerate(resampled_points):
        p.id = index + 35
    return resampled_points


@pytest.mark.parametrize(
    (
        "money_management_strategy_id",
        "long_operation_points",
        "short_operation_points",
        "indicators",
        "resampled_points",
    ),
    [
        # Empty inputs
        (
            1,
            [],
            generate_random_short_operation_points(1, "EURUSD", "2023-11-15", 5),
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 5),
            [],
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 5),
            generate_random_short_operation_points(1, "EURUSD", "2023-11-15", 5),
            [],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 5),
            generate_random_short_operation_points(1, "EURUSD", "2023-11-15", 5),
            [*generate_rsi_indicators(2)],
            [],
        ),
        # instrument mismatch
        (
            1,
            generate_random_long_operation_points(1, "USDCAD", "2023-11-15", 1)
            + generate_random_long_operation_points(1, "EURUSD", "2023-11-16", 4),
            generate_random_short_operation_points(1, "EURUSD", "2023-11-15", 5),
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        # date mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 5),
            generate_random_short_operation_points(1, "EURUSD", "2023-12-15", 5),
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        # money management strategy mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 1)
            + generate_random_long_operation_points(2, "EURUSD", "2023-11-16", 4),
            generate_random_short_operation_points(2, "EURUSD", "2023-11-15", 5),
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        # indicator type mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 5),
            generate_random_short_operation_points(1, "EURUSD", "2023-11-15", 5),
            [*generate_rsi_indicators(2), *generate_macd_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        # resampled points instrument mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-15", 5),
            generate_random_short_operation_points(1, "EURUSD", "2023-11-15", 5),
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "USDCAD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
        # resampled points date mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2023-11-10", 20),
            generate_random_short_operation_points(1, "EURUSD", "2023-11-10", 20),
            [*generate_rsi_indicators(2)],
            generate_resampled_points(
                get_resampled_d1_data(
                    "EURUSD",
                    string_to_datetime("2023-11-13"),
                    string_to_datetime("2023-11-27"),
                )
            ),
        ),
    ],
)
def test_process_strategies_validator_returns_error(  # noqa: PLR0913
    money_management_strategy_id,
    long_operation_points,
    short_operation_points,
    indicators,
    resampled_points,
    rust_endpoint,
):
    data = {
        "money_management_strategy_id": money_management_strategy_id,
        "long_operation_points": [p.to_request_format() for p in long_operation_points],
        "short_operation_points": [p.to_request_format() for p in short_operation_points],
        "indicators": [i.to_request_format() for i in indicators],
        "resampled_points": [i.to_request_format() for i in resampled_points],
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
        "2023-11-15",
        5,
    )

    short_operation_points = generate_random_short_operation_points(
        money_management_strategy_id,
        "EURUSD",
        "2023-11-15",
        5,
    )

    resampled_points = generate_resampled_points(
        get_resampled_d1_data(
            "EURUSD",
            string_to_datetime("2023-11-13"),
            string_to_datetime("2023-11-27"),
        )
    )

    data = {
        "money_management_strategy_id": money_management_strategy_id,
        "long_operation_points": [p.to_request_format() for p in long_operation_points],
        "short_operation_points": [p.to_request_format() for p in short_operation_points],
        "indicators": [i.to_request_format() for i in generate_rsi_indicators(2)],
        "resampled_points": [i.to_request_format() for i in resampled_points],
    }

    response = requests.post(
        url=rust_endpoint("process_strategies_validator"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content.get("data") == "OK!"
