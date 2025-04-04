from views.money_management_strategy.create_multiple_view import (
    MoneyManagementStrategyCreateMultipleView,
)


def test_create_multiple(
    money_management_strategy_schemas,
    money_management_strategies,
):
    assert (
        MoneyManagementStrategyCreateMultipleView(money_management_strategy_schemas).run()
        == money_management_strategies
    )
