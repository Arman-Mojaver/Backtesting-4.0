import pytest

from database.models import Indicator, MoneyManagementStrategy
from database.models.strategy import Strategy
from fixtures.helpers import generate_identifier


@pytest.fixture
def money_management_strategy(session):
    money_management_strategy_data = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
        "risk": 0.02,
    }

    money_management_strategy = MoneyManagementStrategy(
        **money_management_strategy_data,
        identifier=generate_identifier(money_management_strategy_data),
    )

    session.add(money_management_strategy)
    session.commit()

    yield money_management_strategy

    session.query(MoneyManagementStrategy).delete()
    session.commit()


@pytest.fixture
def indicator(session):
    indicator_data = {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }

    indicator = Indicator(**indicator_data)

    session.add(indicator)
    session.commit()

    yield indicator

    session.query(Indicator).delete()
    session.commit()


@pytest.fixture
def strategy_data():
    return {
        "annual_roi": 0.15,
        "max_draw_down": 0.19,
        "annual_operation_count": 4.2,
    }


def test_create_strategy(
    strategy_data,
    money_management_strategy,
    indicator,
    session,
):
    strategy = Strategy(
        **strategy_data,
        money_management_strategy_id=money_management_strategy.id,
        indicator_id=indicator.id,
    )

    session.add(strategy)
    session.commit()

    assert strategy.id
    assert strategy.to_dict() == strategy_data

    session.delete(strategy)
    session.commit()


@pytest.fixture
def strategy(
    money_management_strategy,
    indicator,
    strategy_data,
    session,
):
    strategy_1 = Strategy(
        **strategy_data,
        money_management_strategy_id=money_management_strategy.id,
        indicator_id=indicator.id,
    )
    session.add(strategy_1)
    session.commit()

    return strategy_1


def test_delete_strategy(strategy, session):
    strategy_id = strategy.id

    strategy.delete()
    session.commit()

    assert not session.query(Strategy).filter_by(id=strategy_id).one_or_none()
