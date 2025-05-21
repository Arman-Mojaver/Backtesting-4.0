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

    long_ids = [p.id for p in long_operation_points]
    short_ids = [p.id for p in short_operation_points]

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

    expected_operation_points = [
        long_operation_points_table[0][1],
        short_operation_points_table[1][1],
        long_operation_points_table[2][1],
        short_operation_points_table[3][1],
        long_operation_points_table[4][1],
    ]

    expected_long_ids = [long_ids[0], long_ids[2], long_ids[4]]
    expected_short_ids = [short_ids[1], short_ids[3]]

    response = requests.post(
        url=rust_endpoint("operation_points_filter"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content.get("data") == {
        "operation_points": expected_operation_points,
        "long_operation_point_ids": expected_long_ids,
        "short_operation_point_ids": expected_short_ids,
    }


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

    long_ids = [p.id for p in long_operation_points]
    short_ids = [p.id for p in short_operation_points]

    data = {
        "long_operation_points_table": long_operation_points_table,
        "short_operation_points_table": short_operation_points_table,
        "signal_group": signal_group.to_request_format(),
    }

    expected_operation_points = [
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

    expected_long_ids = [
        long_ids[0],
        long_ids[2],
        long_ids[4],
        long_ids[-5],
        long_ids[-3],
        long_ids[-1],
    ]
    expected_short_ids = [
        short_ids[1],
        short_ids[3],
        short_ids[-6],
        short_ids[-4],
        short_ids[-2],
    ]

    response = requests.post(
        url=rust_endpoint("operation_points_filter"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content.get("data") == {
        "operation_points": expected_operation_points,
        "long_operation_point_ids": expected_long_ids,
        "short_operation_point_ids": expected_short_ids,
    }


def test_operation_points_filter_3(rust_endpoint):
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2025-01-01",
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    long_ids = [p.id for p in long_operation_points]
    short_ids = [p.id for p in short_operation_points]

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

    expected_operation_points = [
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

    expected_long_ids = [
        long_ids[0],
        long_ids[2],
        long_ids[4],
        long_ids[15],
        long_ids[105],
        long_ids[205],
        long_ids[-5],
        long_ids[-3],
        long_ids[-1],
    ]
    expected_short_ids = [
        short_ids[1],
        short_ids[3],
        short_ids[10],
        short_ids[100],
        short_ids[200],
        short_ids[-6],
        short_ids[-4],
        short_ids[-2],
    ]

    response = requests.post(
        url=rust_endpoint("operation_points_filter"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content.get("data") == {
        "operation_points": expected_operation_points,
        "long_operation_point_ids": expected_long_ids,
        "short_operation_point_ids": expected_short_ids,
    }
