import pytest

from views.process_strategies.create_strategies_view import (
    CreateStrategiesView,
    NonExistentIdError,
)

NON_EXISTENT_ID = 123456789


def test_non_existent_money_management_strategies_raises_error(
    strategy_response_defaults,
    indicator,
):
    data = strategy_response_defaults()
    data["strategy_data"]["indicator_id"] = indicator.id

    with pytest.raises(NonExistentIdError):
        CreateStrategiesView(
            [data],
            [],
            [indicator.id],
            [],
            [],
        ).run()


def test_non_existent_indicator_id_raises_error(
    strategy_response_defaults,
    money_management_strategy,
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

    data = strategy_response_defaults()
    data["strategy_data"]["money_management_strategy_id"] = money_management_strategy.id
    data["long_operation_point_ids"] = long_operation_point_ids
    data["short_operation_point_ids"] = short_operation_point_ids

    with pytest.raises(NonExistentIdError):
        CreateStrategiesView(
            [data],
            [money_management_strategy.id],
            [],
            [],
            [],
        ).run()


def test_non_existent_long_operation_point_id_raises_error(
    strategy_response_defaults,
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

    data = strategy_response_defaults()
    data["strategy_data"]["money_management_strategy_id"] = money_management_strategy.id
    data["strategy_data"]["indicator_id"] = indicator.id
    data["long_operation_point_ids"] = [*long_operation_point_ids, NON_EXISTENT_ID]
    data["short_operation_point_ids"] = short_operation_point_ids

    with pytest.raises(NonExistentIdError):
        CreateStrategiesView(
            [data],
            [money_management_strategy.id],
            [indicator.id],
            long_operation_points,
            short_operation_points,
        ).run()


def test_non_existent_short_operation_point_id_raises_error(
    strategy_response_defaults,
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

    data = strategy_response_defaults()
    data["strategy_data"]["money_management_strategy_id"] = money_management_strategy.id
    data["strategy_data"]["indicator_id"] = indicator.id
    data["long_operation_point_ids"] = long_operation_point_ids
    data["short_operation_point_ids"] = [*short_operation_point_ids, NON_EXISTENT_ID]

    with pytest.raises(NonExistentIdError):
        CreateStrategiesView(
            [data],
            [money_management_strategy.id],
            [indicator.id],
            long_operation_points,
            short_operation_points,
        ).run()
