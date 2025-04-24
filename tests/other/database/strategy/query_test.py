from database.models import Indicator, MoneyManagementStrategy, Strategy
from testing_utils.set_utils import set_of_tuples


def test_all_with_empty_table():
    assert Strategy.query.all() == []


def test_all_with_table_items(other_strategies):
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples(other_strategies)


def test_indicator_relationship(other_strategies, session):
    strategy_1, *_ = other_strategies

    queried_indicator = (
        session.query(Indicator).filter_by(id=strategy_1.indicator_id).first()
    )
    assert strategy_1.indicator.to_tuple() == queried_indicator.to_tuple()


def test_money_management_strategy_relationship(other_strategies, session):
    strategy_1, *_ = other_strategies

    queried_money_management_strategy = (
        session.query(MoneyManagementStrategy)
        .filter_by(id=strategy_1.money_management_strategy_id)
        .first()
    )
    assert (
        strategy_1.money_management_strategy.to_tuple()
        == queried_money_management_strategy.to_tuple()
    )
