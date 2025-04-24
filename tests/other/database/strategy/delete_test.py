from database.models import Strategy


def test_delete_through_indicator_relationship(other_strategies, indicator, session):
    indicator_id = indicator.id
    session.delete(indicator)
    session.commit()

    assert session.query(Strategy).filter_by(indicator_id=indicator_id).all() == []


def test_delete_through_money_management_strategy_relationship(
    other_strategies,
    money_management_strategy,
    session,
):
    money_management_strategy_id = money_management_strategy.id
    session.delete(money_management_strategy)
    session.commit()

    assert (
        session.query(Strategy)
        .filter_by(money_management_strategy_id=money_management_strategy_id)
        .all()
        == []
    )
