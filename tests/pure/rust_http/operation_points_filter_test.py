import requests

from models.signals import SignalGroup
from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFactory,
)


def test_operation_points_filter_1(rust_endpoint):
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-05",
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    dates = long_operation_points.dates()

    signal_group = SignalGroup(
        long_signals=[dates[0], dates[2], dates[4]],
        short_signals=[dates[1], dates[3]],
    )

    long_operation_points_table = [
        (item["timestamp"], item) for item in long_operation_points.to_request_format()
    ]
    short_operation_points_table = [
        (item["timestamp"], item) for item in short_operation_points.to_request_format()
    ]

    data = {
        "long_operation_points_table": long_operation_points_table,
        "short_operation_points_table": short_operation_points_table,
        "signal_group": signal_group.to_request_format(),
    }

    expected_result = [
        long_operation_points_table[0][1],
        short_operation_points_table[1][1],
        long_operation_points_table[2][1],
        short_operation_points_table[3][1],
        long_operation_points_table[4][1],
    ]

    response = requests.post(
        url=rust_endpoint("operation_points_filter"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content["data"] == expected_result


def test_operation_points_filter_2(rust_endpoint):
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-02-01",
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    dates = long_operation_points.dates()

    signal_group = SignalGroup(
        long_signals=[
            dates[0],
            dates[2],
            dates[4],
            dates[-5],
            dates[-3],
            dates[-1],
        ],
        short_signals=[
            dates[1],
            dates[3],
            dates[-6],
            dates[-4],
            dates[-2],
        ],
    )

    long_operation_points_table = [
        (item["timestamp"], item) for item in long_operation_points.to_request_format()
    ]
    short_operation_points_table = [
        (item["timestamp"], item) for item in short_operation_points.to_request_format()
    ]

    data = {
        "long_operation_points_table": long_operation_points_table,
        "short_operation_points_table": short_operation_points_table,
        "signal_group": signal_group.to_request_format(),
    }

    expected_result = [
        long_operation_points_table[0][1],
        short_operation_points_table[1][1],
        long_operation_points_table[2][1],
        short_operation_points_table[3][1],
        long_operation_points_table[4][1],
        short_operation_points_table[-6][1],
        long_operation_points_table[-5][1],
        short_operation_points_table[-4][1],
        long_operation_points_table[-3][1],
        short_operation_points_table[-2][1],
        long_operation_points_table[-1][1],
    ]

    response = requests.post(
        url=rust_endpoint("operation_points_filter"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content["data"] == expected_result


def test_operation_points_filter_3(rust_endpoint):
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2025-01-01",
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    dates = long_operation_points.dates()

    signal_group = SignalGroup(
        long_signals=[
            dates[0],
            dates[2],
            dates[4],
            dates[15],
            dates[105],
            dates[205],
            dates[-5],
            dates[-3],
            dates[-1],
        ],
        short_signals=[
            dates[1],
            dates[3],
            dates[10],
            dates[100],
            dates[200],
            dates[-6],
            dates[-4],
            dates[-2],
        ],
    )

    long_operation_points_table = [
        (item["timestamp"], item) for item in long_operation_points.to_request_format()
    ]
    short_operation_points_table = [
        (item["timestamp"], item) for item in short_operation_points.to_request_format()
    ]

    data = {
        "long_operation_points_table": long_operation_points_table,
        "short_operation_points_table": short_operation_points_table,
        "signal_group": signal_group.to_request_format(),
    }

    expected_result = [
        long_operation_points_table[0][1],
        short_operation_points_table[1][1],
        long_operation_points_table[2][1],
        short_operation_points_table[3][1],
        long_operation_points_table[4][1],
        short_operation_points_table[10][1],
        long_operation_points_table[15][1],
        short_operation_points_table[100][1],
        long_operation_points_table[105][1],
        short_operation_points_table[200][1],
        long_operation_points_table[205][1],
        short_operation_points_table[-6][1],
        long_operation_points_table[-5][1],
        short_operation_points_table[-4][1],
        long_operation_points_table[-3][1],
        short_operation_points_table[-2][1],
        long_operation_points_table[-1][1],
    ]

    response = requests.post(
        url=rust_endpoint("operation_points_filter"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content["data"] == expected_result
