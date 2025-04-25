from database.models.money_management_strategy import MoneyManagementStrategyList


def test_get_ids(money_management_strategies):
    assert MoneyManagementStrategyList([]).get_ids() == set()
    assert MoneyManagementStrategyList(money_management_strategies).get_ids() == {
        m.id for m in money_management_strategies
    }
