from datetime import datetime

import pytest
import requests

from models.signals import SignalGroup
from testing_utils.finance_utils.annual_operation_count import (
    calculate_annual_operation_count,
)
from testing_utils.finance_utils.annual_roi import calculate_annual_roi
from testing_utils.finance_utils.draw_down import calculate_max_draw_down
from testing_utils.finance_utils.global_roi import calculate_global_roi
from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFactory,
)
from utils.date_utils import datetime_to_string


@pytest.mark.parametrize(
    "end_date", ["2024-07-01", "2025-01-01", "2025-07-01", "2026-01-01"]
)
@pytest.mark.parametrize(
    ("long_date_indices", "short_date_indices"),
    [
        ((0, 2, 4), (1, 3)),
        ((0, 2, 4), (1, 3, 5)),
        ((1, 3), (0, 2, 4)),
        ((1, 3, 5), (0, 2, 4)),
        ((0, 2, 4, -4, -2), (1, 3, 5, -3, -1)),
    ],
)
def test_process_strategy(end_date, long_date_indices, short_date_indices, rust_endpoint):
    instrument, money_management_strategy_id, indicator_id = "EURUSD", 1, 20
    operation_points_factory = OperationPointsFactory(
        instrument=instrument,
        mm_strategy_id=money_management_strategy_id,
        start_date="2024-01-01",
        end_date=end_date,
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    dates = long_operation_points.dates()

    signal_group = SignalGroup(
        long_signals=[dates[index] for index in long_date_indices],
        short_signals=[dates[index] for index in short_date_indices],
    )

    long_operation_points_table = [
        (item["timestamp"], item) for item in long_operation_points.to_request_format()
    ]
    short_operation_points_table = [
        (item["timestamp"], item) for item in short_operation_points.to_request_format()
    ]

    start_date = datetime_to_string(datetime.fromtimestamp(dates[0]))  # noqa: DTZ006
    end_date = datetime_to_string(datetime.fromtimestamp(dates[-1]))  # noqa: DTZ006

    data = {
        "instrument": instrument,
        "long_operation_points_table": long_operation_points_table,
        "short_operation_points_table": short_operation_points_table,
        "signal_group": signal_group.to_request_format(),
        "start_date": dates[0],
        "end_date": dates[-1],
        "money_management_strategy_id": money_management_strategy_id,
        "indicator_id": indicator_id,
    }

    response = requests.post(
        url=rust_endpoint("process_strategy_test"),
        json=data,
        timeout=5,
    )

    long_operation_points_map_obj = {
        item.timestamp: item for item in long_operation_points
    }
    short_operation_points_map_obj = {
        item.timestamp: item for item in short_operation_points
    }

    long_operation_points = [
        long_operation_points_map_obj[dates[index]] for index in long_date_indices
    ]
    short_operation_points = [
        short_operation_points_map_obj[dates[index]] for index in short_date_indices
    ]

    long_operation_point_ids = [p.id for p in long_operation_points]
    short_operation_point_ids = [p.id for p in short_operation_points]

    operation_points = sorted(
        [*long_operation_points, *short_operation_points], key=lambda p: p.timestamp
    )

    content = parse_response(response)

    expected_annual_operation_count = calculate_annual_operation_count(
        start_date,
        end_date,
        operation_points,
    )
    expected_max_draw_down = calculate_max_draw_down(operation_points)
    expected_annual_roi = calculate_annual_roi(
        start_date,
        end_date,
        calculate_global_roi(operation_points),
    )

    # TODO: Fix or reduce rounding error  # noqa: FIX002, TD002, TD003
    assert (
        abs(
            content.get("data", {})["strategy"]["annual_operation_count"]
            - expected_annual_operation_count
        )
        <= 0.3
    )
    assert content.get("data", {})["strategy"]["max_draw_down"] == expected_max_draw_down
    assert content.get("data", {})["strategy"]["annual_roi"] == expected_annual_roi
    assert (
        content.get("data", {})["strategy"]["money_management_strategy_id"]
        == money_management_strategy_id
    )
    assert content.get("data", {})["strategy"]["indicator_id"] == indicator_id
    assert content.get("data", {})["long_operation_point_ids"] == long_operation_point_ids
    assert (
        content.get("data", {})["short_operation_point_ids"] == short_operation_point_ids
    )
