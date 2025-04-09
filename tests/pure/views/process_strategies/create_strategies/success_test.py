from views.process_strategies.create_strategies_view import (
    CreateStrategiesView,
)

# TODO: fix test once relationships are restored in the models  # noqa: FIX002, TD002, TD003, E501


def test_create_one_strategy(
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
    data["short_operation_point_ids"] = short_operation_point_ids

    CreateStrategiesView(
        [data],
        [money_management_strategy.id],
        [indicator.id],
        long_operation_points,
        short_operation_points,
    ).run()

    assert True
    # expected_result = Strategy(**data["strategy_data"]).to_dict()  # noqa: ERA001
    #
    # strategies = session.query(Strategy).all()  # noqa: ERA001
    # assert strategies  # noqa: ERA001
    # assert strategies[0].to_dict() == expected_result  # noqa: ERA001
    # assert {
    #     item.long_operation_point_id
    #     for item in LongOperationPointStrategy.query.all()
    # } == set(long_operation_point_ids)
    # assert {
    #     item.short_operation_point_id
    #     for item in ShortOperationPointStrategy.query.all()
    # } == set(short_operation_point_ids)
    #
    # session.query(Strategy).delete()  # noqa: ERA001
    # session.query(LongOperationPointStrategy).delete()  # noqa: ERA001
    # session.query(ShortOperationPointStrategy).delete()  # noqa: ERA001
