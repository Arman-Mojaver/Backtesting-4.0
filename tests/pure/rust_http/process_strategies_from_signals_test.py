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
    "end_date",
    ["2024-07-01", "2025-01-01", "2025-07-01", "2026-01-01"],
)
@pytest.mark.parametrize(
    "signal_groups_data",
    [
        (
            ((0, 2, 4), (1, 3)),
            ((0, 2, 4), (1, 3, 5)),
        ),
        (
            ((0, 2, 4), (1, 3)),
            ((0, 2, 4, -4, -2), (1, 3, 5, -3, -1)),
        ),
    ],
)
def test_process_strategies(
    end_date,
    signal_groups_data,
    rust_endpoint,
):
    instrument = "EURUSD"
    money_management_strategy_id = 1
    operation_points_factory = OperationPointsFactory(
        instrument=instrument,
        mm_strategy_id=money_management_strategy_id,
        start_date="2024-01-01",
        end_date=end_date,
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    dates = long_operation_points.dates()

    signal_group_data_1, signal_group_data_2 = signal_groups_data

    long_date_indices_1, short_date_indices_1 = (
        signal_group_data_1[0],
        signal_group_data_1[1],
    )

    long_date_indices_2, short_date_indices_2 = (
        signal_group_data_2[0],
        signal_group_data_2[1],
    )

    signal_group_1 = SignalGroup(
        long_signals=[dates[index] for index in long_date_indices_1],
        short_signals=[dates[index] for index in short_date_indices_1],
    )

    signal_group_2 = SignalGroup(
        long_signals=[dates[index] for index in long_date_indices_2],
        short_signals=[dates[index] for index in short_date_indices_2],
    )

    start_date = datetime_to_string(datetime.fromtimestamp(dates[0]))  # noqa: DTZ006
    end_date = datetime_to_string(datetime.fromtimestamp(dates[-1]))  # noqa: DTZ006

    data = {
        "instrument": instrument,
        "long_operation_points": long_operation_points.to_request_format(),
        "short_operation_points": short_operation_points.to_request_format(),
        "signal_groups": {
            21: signal_group_1.to_request_format(),
            22: signal_group_2.to_request_format(),
        },
        "money_management_strategy_id": money_management_strategy_id,
    }

    response = requests.post(
        url=rust_endpoint("process_strategies_from_signals_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    long_operation_points_map_obj = {
        item.timestamp: item for item in long_operation_points
    }
    short_operation_points_map_obj = {
        item.timestamp: item for item in short_operation_points
    }

    # 1

    long_operation_points_1 = [
        long_operation_points_map_obj[dates[index]] for index in long_date_indices_1
    ]
    short_operation_points_1 = [
        short_operation_points_map_obj[dates[index]] for index in short_date_indices_1
    ]

    long_operation_point_ids_1 = [p.id for p in long_operation_points_1]
    short_operation_point_ids_1 = [p.id for p in short_operation_points_1]

    operation_points_1 = sorted(
        [*long_operation_points_1, *short_operation_points_1], key=lambda p: p.timestamp
    )

    expected_annual_operation_count_1 = calculate_annual_operation_count(
        start_date,
        end_date,
        operation_points_1,
    )
    expected_max_draw_down_1 = calculate_max_draw_down(operation_points_1)
    expected_annual_roi_1 = calculate_annual_roi(
        start_date,
        end_date,
        calculate_global_roi(operation_points_1),
    )

    # 2

    long_operation_points_2 = [
        long_operation_points_map_obj[dates[index]] for index in long_date_indices_2
    ]
    short_operation_points_2 = [
        short_operation_points_map_obj[dates[index]] for index in short_date_indices_2
    ]

    long_operation_point_ids_2 = [p.id for p in long_operation_points_2]
    short_operation_point_ids_2 = [p.id for p in short_operation_points_2]

    operation_points_2 = sorted(
        [*long_operation_points_2, *short_operation_points_2], key=lambda p: p.timestamp
    )

    expected_annual_operation_count_2 = calculate_annual_operation_count(
        start_date,
        end_date,
        operation_points_2,
    )
    expected_max_draw_down_2 = calculate_max_draw_down(operation_points_2)
    expected_annual_roi_2 = calculate_annual_roi(
        start_date,
        end_date,
        calculate_global_roi(operation_points_2),
    )

    # TODO: Fix or reduce rounding error  # noqa: FIX002, TD002, TD003
    assert (
        abs(
            content.get("data", [])[0]["strategy"]["annual_operation_count"]
            - expected_annual_operation_count_1
        )
        <= 0.3
    )
    assert (
        content.get("data", [])[0]["strategy"]["max_draw_down"]
        == expected_max_draw_down_1
    )
    assert content.get("data", [])[0]["strategy"]["annual_roi"] == expected_annual_roi_1
    assert (
        content.get("data", [])[0]["strategy"]["money_management_strategy_id"]
        == money_management_strategy_id
    )
    assert content.get("data", [])[0]["strategy"]["indicator_id"] == 21
    assert (
        content.get("data", [])[0]["long_operation_point_ids"]
        == long_operation_point_ids_1
    )
    assert (
        content.get("data", [])[0]["short_operation_point_ids"]
        == short_operation_point_ids_1
    )

    # TODO: Fix or reduce rounding error  # noqa: FIX002, TD002, TD003
    assert (
        abs(
            content.get("data", [])[1]["strategy"]["annual_operation_count"]
            - expected_annual_operation_count_2
        )
        <= 0.3
    )
    assert (
        content.get("data", [])[1]["strategy"]["max_draw_down"]
        == expected_max_draw_down_2
    )
    assert content.get("data", [])[1]["strategy"]["annual_roi"] == expected_annual_roi_2
    assert (
        content.get("data", [])[1]["strategy"]["money_management_strategy_id"]
        == money_management_strategy_id
    )
    assert content.get("data", [])[1]["strategy"]["indicator_id"] == 22
    assert (
        content.get("data", [])[1]["long_operation_point_ids"]
        == long_operation_point_ids_2
    )
    assert (
        content.get("data", [])[1]["short_operation_point_ids"]
        == short_operation_point_ids_2
    )
