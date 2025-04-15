from database.models.money_management_strategy import MoneyManagementStrategyList


def test_long_operation_points_empty(money_management_strategies):
    assert (
        MoneyManagementStrategyList(money_management_strategies).long_operation_points()
        == []
    )


def test_long_operation_points(money_management_strategies_with_long_operation_points):
    expected_result = [
        long_op_point
        for m in money_management_strategies_with_long_operation_points
        for long_op_point in m.long_operation_points
    ]

    assert (
        MoneyManagementStrategyList(
            money_management_strategies_with_long_operation_points
        ).long_operation_points()
        == expected_result
    )


def test_short_operation_points_empty(money_management_strategies):
    assert (
        MoneyManagementStrategyList(money_management_strategies).short_operation_points()
        == []
    )


def test_short_operation_points(money_management_strategies_with_short_operation_points):
    expected_result = [
        short_op_point
        for m in money_management_strategies_with_short_operation_points
        for short_op_point in m.short_operation_points
    ]

    assert (
        MoneyManagementStrategyList(
            money_management_strategies_with_short_operation_points
        ).short_operation_points()
        == expected_result
    )


def test_get_ids(money_management_strategies):
    assert MoneyManagementStrategyList([]).get_ids() == []
    assert MoneyManagementStrategyList(money_management_strategies).get_ids() == [
        m.id for m in money_management_strategies
    ]
