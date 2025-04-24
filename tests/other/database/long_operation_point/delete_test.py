from database.models import LongOperationPoint


def test_delete_strategy_does_not_delete_long_operation_point(
    strategy_with_long_operation_points,
    other_long_operation_points,
    session,
):
    strategies = [
        strategy for point in other_long_operation_points for strategy in point.strategies
    ]

    for strategy in strategies:
        session.delete(strategy)
    session.commit()

    assert session.query(LongOperationPoint).all() == other_long_operation_points
