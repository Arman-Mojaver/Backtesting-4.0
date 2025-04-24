from database.models import ShortOperationPoint


def test_delete_strategy_does_not_delete_short_operation_point(
    strategy_with_short_operation_points,
    other_short_operation_points,
    session,
):
    strategies = [
        strategy
        for point in other_short_operation_points
        for strategy in point.strategies
    ]

    for strategy in strategies:
        session.delete(strategy)
    session.commit()

    assert session.query(ShortOperationPoint).all() == other_short_operation_points
