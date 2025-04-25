import pytest

from views.process_strategies.create_strategies_view import (
    CreateStrategiesView,
    MismatchedIdError,
)


def test_strategy_does_not_match_operation_points(
    strategy_response_defaults,
    money_management_strategies,
    indicator,
    generate_long_operation_points,
    generate_short_operation_points,
):
    mm_strategy_1, mm_strategy_2 = money_management_strategies

    long_operation_points = generate_long_operation_points(
        money_management_strategy_id=mm_strategy_1.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    long_operation_point_ids = [item.id for item in long_operation_points]

    short_operation_points = generate_short_operation_points(
        money_management_strategy_id=mm_strategy_1.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    short_operation_point_ids = [item.id for item in short_operation_points]

    data = strategy_response_defaults()
    data["strategy_data"]["money_management_strategy_id"] = mm_strategy_2.id
    data["strategy_data"]["indicator_id"] = indicator.id
    data["long_operation_point_ids"] = long_operation_point_ids
    data["short_operation_point_ids"] = short_operation_point_ids

    with pytest.raises(MismatchedIdError):
        CreateStrategiesView(
            [data],
            mm_strategy_2.id,
            [indicator.id],
            long_operation_points,
            short_operation_points,
        ).run()


def test_long_operation_point_id_does_not_match_the_rest(
    strategy_response_defaults,
    money_management_strategies,
    indicator,
    generate_long_operation_points,
    generate_short_operation_points,
):
    mm_strategy_1, mm_strategy_2 = money_management_strategies

    long_operation_points = generate_long_operation_points(
        money_management_strategy_id=mm_strategy_2.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    long_operation_point_ids = [item.id for item in long_operation_points]

    short_operation_points = generate_short_operation_points(
        money_management_strategy_id=mm_strategy_1.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    short_operation_point_ids = [item.id for item in short_operation_points]

    data = strategy_response_defaults()
    data["strategy_data"]["money_management_strategy_id"] = mm_strategy_1.id
    data["strategy_data"]["indicator_id"] = indicator.id
    data["long_operation_point_ids"] = long_operation_point_ids
    data["short_operation_point_ids"] = short_operation_point_ids

    with pytest.raises(MismatchedIdError):
        CreateStrategiesView(
            [data],
            mm_strategy_1.id,
            [indicator.id],
            long_operation_points,
            short_operation_points,
        ).run()


def test_short_operation_point_id_does_not_match_the_rest(
    strategy_response_defaults,
    money_management_strategies,
    indicator,
    generate_long_operation_points,
    generate_short_operation_points,
):
    mm_strategy_1, mm_strategy_2 = money_management_strategies

    long_operation_points = generate_long_operation_points(
        money_management_strategy_id=mm_strategy_1.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    long_operation_point_ids = [item.id for item in long_operation_points]

    short_operation_points = generate_short_operation_points(
        money_management_strategy_id=mm_strategy_2.id,
        instrument="EURUSD",
        start_date="2024-01-01",
        count=2,
    )
    short_operation_point_ids = [item.id for item in short_operation_points]

    data = strategy_response_defaults()
    data["strategy_data"]["money_management_strategy_id"] = mm_strategy_1.id
    data["strategy_data"]["indicator_id"] = indicator.id
    data["long_operation_point_ids"] = long_operation_point_ids
    data["short_operation_point_ids"] = short_operation_point_ids

    with pytest.raises(MismatchedIdError):
        CreateStrategiesView(
            [data],
            mm_strategy_1.id,
            [indicator.id],
            long_operation_points,
            short_operation_points,
        ).run()
