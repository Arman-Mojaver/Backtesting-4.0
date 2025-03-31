import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory import (
    ProcessStrategiesRequestBodyFactory,
    StrategyResponseOperationCount,
)

INSTRUMENT = "EURUSD"


@pytest.mark.parametrize(
    (
        "end_date",
        "long_signals_counts",
        "short_signals_counts",
        "expected_results",
    ),
    [
        ("2025-01-01", [0], [0], [0.0]),
        ("2025-01-01", [1], [0], [1.0]),
        ("2025-01-01", [0], [1], [1.0]),
        ("2025-01-01", [1], [1], [2.0]),
        ("2026-01-01", [1], [1], [1.0]),
        ("2026-01-01", [1], [0], [0.5]),
        ("2026-01-01", [0], [1], [0.5]),
        ("2026-01-01", [2], [1], [1.5]),
        ("2026-01-01", [1], [2], [1.5]),
        ("2026-01-01", [2], [2], [2.0]),
        ("2025-01-01", [1, 1], [1, 0], [2.0, 1.0]),
        ("2026-01-01", [0, 1, 1, 2, 2], [0, 0, 1, 1, 2], [0.0, 0.5, 1.0, 1.5, 2.0]),
    ],
)
@pytest.mark.parametrize("money_management_strategy_count", [1, 2, 3])
def test_annual_operation_count(  # noqa: PLR0913
    end_date,
    long_signals_counts,
    short_signals_counts,
    expected_results,
    money_management_strategy_count,
    endpoint,
):
    request_body = ProcessStrategiesRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_count=money_management_strategy_count,
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
        StrategyResponseOperationCount.model_validate(data)
        for data in response_content["data"]
    ]
    expected_strategy_responses = request_body.strategy_responses()

    annual_operation_counts = [
        strategy_response.strategy_data.annual_operation_count
        for strategy_response in strategy_responses
    ]

    assert (
        len(response_content["data"])
        == len(expected_results) * money_management_strategy_count
    )
    assert set(strategy_responses) == set(expected_strategy_responses)
    assert set(annual_operation_counts) == set(expected_results)
