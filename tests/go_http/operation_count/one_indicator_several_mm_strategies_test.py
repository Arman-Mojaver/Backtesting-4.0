import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory import (
    ProcessStrategiesRequestBodyFactory,
    StrategyResponse,
)

INSTRUMENT = "EURUSD"


@pytest.mark.parametrize(
    (
        "end_date",
        "long_signals_counts",
        "short_signals_counts",
        "expected_result",
    ),
    [
        ("2025-01-01", [1], [1], 2.0),
        ("2025-01-01", [1], [0], 1.0),
        ("2025-01-01", [0], [1], 1.0),
        ("2026-01-01", [1], [1], 1.0),
        ("2026-01-01", [1], [0], 0.5),
        ("2026-01-01", [0], [1], 0.5),
        ("2026-01-01", [2], [1], 1.5),
        ("2026-01-01", [1], [2], 1.5),
        ("2026-01-01", [2], [2], 2.0),
    ],
)
def test_annual_operation_count(
    end_date,
    long_signals_counts,
    short_signals_counts,
    expected_result,
    endpoint,
):
    request_body = ProcessStrategiesRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_count=2,
        start_date="2024-01-01",
        long_signals_counts=long_signals_counts,
        short_signals_counts=short_signals_counts,
        end_date=end_date,
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)
    strategy_responses = [
        StrategyResponse.model_validate(data) for data in response_content["data"]
    ]
    expected_strategy_responses = request_body.strategy_responses()

    annual_operation_counts = [
        strategy_response.strategy_data.annual_operation_count
        for strategy_response in strategy_responses
    ]

    assert len(response_content["data"]) == 2
    assert set(strategy_responses) == set(expected_strategy_responses)
    assert set(annual_operation_counts) == {expected_result}
