import time

import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFactory,
)
from testing_utils.request_body_factory.signal_group_factory import SignalGroupFactory

INDICATOR_COUNT = 10000
SAMPLE_COUNT = 3000


@pytest.mark.skip(reason="Performance test, takes a long time")
def test_process_strategies_performance(rust_endpoint):
    money_management_strategy_id = 1
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=money_management_strategy_id,
        start_date="2022-01-01",
        end_date="2037-01-01",
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    dates = tuple(long_operation_points.dates())

    signal_group_factory = SignalGroupFactory(
        dates=dates, count=INDICATOR_COUNT, sample_count=SAMPLE_COUNT
    )

    data = {
        "long_operation_points": long_operation_points.to_request_format(),
        "short_operation_points": short_operation_points.to_request_format(),
        "signal_groups": signal_group_factory.to_request_format(),
        "money_management_strategy_id": money_management_strategy_id,
    }

    print("Sending request")  # noqa: T201
    start = time.time()
    response = requests.post(
        url=rust_endpoint("process_strategies"),
        json=data,
        timeout=30,
    )

    elapsed = time.time() - start
    print(f"Request time: {round(elapsed, 2)}s")  # noqa: T201

    content = parse_response(response)
    assert len(content.get("data", [])) == INDICATOR_COUNT

    """
    Single threaded, with clones:
        Request time: 18.65s
        Process time: 8.89s

    Single threaded:
        Request time: 18.8s
        Process time: 8.12s

    Single threaded, with FXHasher:
        Request time: 15.46s
        Process time: 5.21s

    Multithreaded, with FXHasher, with clones:
        Request time: 12.69s
        Process time: 3.71s

    Multithreaded, with FXHasher:
        Request time: 10.77s
        Process time: 1.93s

    Multithreaded, with Dual Linear Scan:
        Request time: 10.74s
        Process time: 1.36s

    """
