from database.models import (
    LongOperationPointStrategy,
    ShortOperationPointStrategy,
    Strategy,
)
from views.process_strategies.create_strategies_view import (
    CreateStrategiesView,
)


def test_create_one_strategy(  # noqa: PLR0913
    strategy_response_defaults,
    money_management_strategy,
    indicator,
    generate_long_operation_points,
    generate_short_operation_points,
    session,
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
    data["short_operation_point_ids"] = short_operation_point_ids

    CreateStrategiesView([data]).run()

    expected_result = Strategy(**data["strategy_data"]).to_dict()

    strategies = session.query(Strategy).all()
    assert strategies
    assert strategies[0].to_dict() == expected_result
    assert {
        item.long_operation_point_id for item in LongOperationPointStrategy.query.all()
    } == set(long_operation_point_ids)
    assert {
        item.short_operation_point_id for item in ShortOperationPointStrategy.query.all()
    } == set(short_operation_point_ids)

    session.query(Strategy).delete()
    session.query(LongOperationPointStrategy).delete()
    session.query(ShortOperationPointStrategy).delete()
