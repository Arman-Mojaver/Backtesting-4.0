from collections import defaultdict

import pytest

from views.process_strategies.load_process_strategies_data import (
    InvalidOperationPointsError,
    LoadProcessStrategiesData,
    OperationPoints,
)


@pytest.fixture
def other_long_operation_points(
    money_management_strategies,
    generate_long_operation_points,
):
    generate_long_operation_points(
        money_management_strategies[0].id,
        "USDCAD",
        "2020-01-01",
        10,
    )

    generate_long_operation_points(
        money_management_strategies[1].id,
        "USDCAD",
        "2020-01-01",
        10,
    )


@pytest.fixture
def other_short_operation_points(
    money_management_strategies,
    generate_short_operation_points,
):
    generate_short_operation_points(
        money_management_strategies[0].id,
        "USDCAD",
        "2020-01-01",
        10,
    )

    generate_short_operation_points(
        money_management_strategies[1].id,
        "USDCAD",
        "2020-01-01",
        10,
    )


@pytest.fixture
def _other_operation_points(
    other_long_operation_points,
    other_short_operation_points,
):
    return


@pytest.mark.usefixtures("_other_operation_points")
def test_long_operations_points_empty():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def _only_long_operation_points(
    money_management_strategies,
    generate_long_operation_points,
):
    generate_long_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        10,
    )


@pytest.mark.usefixtures("_other_operation_points", "_only_long_operation_points")
def test_only_long_operation_points():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def _only_short_operation_points(
    money_management_strategies,
    generate_short_operation_points,
):
    generate_short_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        10,
    )


@pytest.mark.usefixtures("_other_operation_points", "_only_short_operation_points")
def test_only_short_operation_points():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def _date_mismatched_operation_points(
    money_management_strategies,
    generate_long_operation_points,
    generate_short_operation_points,
):
    generate_long_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-10",
        10,
    )

    generate_short_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        10,
    )


@pytest.mark.usefixtures("_other_operation_points", "_date_mismatched_operation_points")
def test_date_mismatched_operation_points():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def _instrument_mismatched_operation_points(
    money_management_strategies,
    generate_long_operation_points,
    generate_short_operation_points,
):
    generate_long_operation_points(
        money_management_strategies[0].id,
        "USDCAD",
        "2024-01-01",
        1,
    )

    generate_long_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-02",
        9,
    )

    generate_short_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        10,
    )


@pytest.mark.usefixtures(
    "_other_operation_points",
    "_instrument_mismatched_operation_points",
)
def test_instrument_mismatched_operation_points():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def _money_management_strategy_mismatched_operation_points(
    money_management_strategies,
    generate_long_operation_points,
    generate_short_operation_points,
):
    generate_long_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        1,
    )

    generate_long_operation_points(
        money_management_strategies[1].id,
        "EURUSD",
        "2024-01-02",
        9,
    )

    generate_short_operation_points(
        money_management_strategies[1].id,
        "EURUSD",
        "2024-01-01",
        10,
    )


@pytest.mark.usefixtures(
    "_other_operation_points",
    "_money_management_strategy_mismatched_operation_points",
)
def test_money_management_strategy_mismatched_operation_points():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def money_management_strategy_and_dates_mismatched_operation_points(
    money_management_strategies,
    generate_long_operation_points,
    generate_short_operation_points,
):
    generate_long_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        2,
    )

    generate_long_operation_points(
        money_management_strategies[1].id,
        "EURUSD",
        "2024-01-04",
        2,
    )

    generate_short_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        2,
    )

    generate_short_operation_points(
        money_management_strategies[1].id,
        "EURUSD",
        "2024-01-04",
        2,
    )


@pytest.mark.usefixtures(
    "_other_operation_points",
    "money_management_strategy_and_dates_mismatched_operation_points",
)
def test_all_mm_strategies_should_have_same_dates():
    with pytest.raises(InvalidOperationPointsError):
        LoadProcessStrategiesData(instrument="EURUSD").run()


@pytest.fixture
def matched_operation_points(
    money_management_strategies,
    generate_long_operation_points,
    generate_short_operation_points,
):
    long_operation_points = generate_long_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        10,
    )

    short_operation_points = generate_short_operation_points(
        money_management_strategies[0].id,
        "EURUSD",
        "2024-01-01",
        10,
    )

    return long_operation_points, short_operation_points


@pytest.mark.usefixtures("_other_operation_points")
def test_matched_operation_points_returns_points(matched_operation_points):
    long_operation_points, short_operation_points = matched_operation_points

    long_operation_points_by_mm_strategy = defaultdict(list)
    for point in long_operation_points:
        long_operation_points_by_mm_strategy[point.money_management_strategy_id].append(
            point
        )

    short_operation_points_by_mm_strategy = defaultdict(list)
    for point in short_operation_points:
        short_operation_points_by_mm_strategy[point.money_management_strategy_id].append(
            point
        )

    assert LoadProcessStrategiesData(
        instrument=long_operation_points[0].instrument
    ).run() == OperationPoints(
        long_operation_points_by_mm_strategy,
        short_operation_points_by_mm_strategy,
    )
