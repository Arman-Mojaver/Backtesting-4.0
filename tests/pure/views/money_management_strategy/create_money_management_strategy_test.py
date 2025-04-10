from testing_utils.set_utils import set_of_tuples
from views.money_management_strategy.create_multiple_view import (
    MoneyManagementStrategyCreateMultipleView,
)


def test_create_multiple(
    money_management_strategy_schemas,
    money_management_strategies,
):
    assert set_of_tuples(
        MoneyManagementStrategyCreateMultipleView(money_management_strategy_schemas).run()
    ) == set_of_tuples(money_management_strategies)
