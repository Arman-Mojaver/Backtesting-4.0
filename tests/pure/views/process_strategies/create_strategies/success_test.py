from database.models import Strategy
from testing_utils.set_utils import set_of_tuples
from views.process_strategies.create_strategies_view import (
    CreateStrategiesView,
)


def test_create_one_strategy(
    money_management_strategy,
    indicator,
    generate_long_operation_points,
    generate_short_operation_points,
):
    long_operation_points = generate_long_operation_points(
        money_management_strategy_id=money_management_strategy.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    long_operation_point_ids = [item.id for item in long_operation_points]

    short_operation_points = generate_short_operation_points(
        money_management_strategy_id=money_management_strategy.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    short_operation_point_ids = [item.id for item in short_operation_points]

    data = {
        "long_operation_point_ids": long_operation_point_ids,
        "short_operation_point_ids": short_operation_point_ids,
        "strategy_data": {
            "annual_roi": 10.0,
            "annual_operation_count": 0.5,
            "max_draw_down": 2.0,
            "indicator_id": indicator.id,
            "money_management_strategy_id": money_management_strategy.id,
        },
    }

    strategies = CreateStrategiesView(
        [data],
        [money_management_strategy.id],
        [indicator.id],
        long_operation_points,
        short_operation_points,
    ).run()

    expected_result = [Strategy(**data["strategy_data"])]

    assert set_of_tuples(strategies) == set_of_tuples(expected_result)
    assert set(long_operation_point_ids) == {
        item.id for item in strategies[0].long_operation_points
    }
    assert set(short_operation_point_ids) == {
        item.id for item in strategies[0].short_operation_points
    }


def test_create_multiple_strategies(
    money_management_strategy,
    indicator,
    indicator_2,
    generate_long_operation_points,
    generate_short_operation_points,
):
    long_operation_points = generate_long_operation_points(
        money_management_strategy_id=money_management_strategy.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=4,
    )
    long_operation_point_ids = [item.id for item in long_operation_points]

    short_operation_points = generate_short_operation_points(
        money_management_strategy_id=money_management_strategy.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=4,
    )
    short_operation_point_ids = [item.id for item in short_operation_points]

    long_operation_point_ids_1 = long_operation_point_ids[:2]
    long_operation_point_ids_2 = long_operation_point_ids[2:]
    short_operation_point_ids_1 = short_operation_point_ids[:3]
    short_operation_point_ids_2 = short_operation_point_ids[3:]

    data_1 = {
        "long_operation_point_ids": long_operation_point_ids_1,
        "short_operation_point_ids": short_operation_point_ids_1,
        "strategy_data": {
            "annual_roi": 10.0,
            "annual_operation_count": 0.5,
            "max_draw_down": 2.0,
            "indicator_id": indicator.id,
            "money_management_strategy_id": money_management_strategy.id,
        },
    }

    data_2 = {
        "long_operation_point_ids": long_operation_point_ids_2,
        "short_operation_point_ids": short_operation_point_ids_2,
        "strategy_data": {
            "annual_roi": 11.0,
            "annual_operation_count": 0.6,
            "max_draw_down": 3.0,
            "indicator_id": indicator_2.id,
            "money_management_strategy_id": money_management_strategy.id,
        },
    }

    strategies = CreateStrategiesView(
        [data_1, data_2],
        [money_management_strategy.id],
        [indicator.id, indicator_2.id],
        long_operation_points,
        short_operation_points,
    ).run()

    expected_result = [
        Strategy(**data_1["strategy_data"]),
        Strategy(**data_2["strategy_data"]),
    ]

    assert set_of_tuples(strategies) == set_of_tuples(expected_result)
    assert set(long_operation_point_ids_1) == {
        item.id for item in strategies[0].long_operation_points
    }
    assert set(short_operation_point_ids_1) == {
        item.id for item in strategies[0].short_operation_points
    }
    assert set(long_operation_point_ids_2) == {
        item.id for item in strategies[1].long_operation_points
    }
    assert set(short_operation_point_ids_2) == {
        item.id for item in strategies[1].short_operation_points
    }
