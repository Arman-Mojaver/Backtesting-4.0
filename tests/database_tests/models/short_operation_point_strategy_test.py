import pytest

from database.models import (
    Indicator,
    MoneyManagementStrategy,
    ShortOperationPoint,
    ShortOperationPointStrategy,
    Strategy,
)


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
        "identifier": "atr-1.5-1.0-14",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy(money_management_strategy_data, session):
    point = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(point)
    session.commit()

    yield point

    session.delete(point)
    session.commit()


@pytest.fixture
def short_operation_point_data():
    return {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
    }


@pytest.fixture
def short_operation_point(short_operation_point_data, money_management_strategy, session):
    point = ShortOperationPoint(
        **short_operation_point_data,
        money_management_strategy_id=money_management_strategy.id,
    )

    session.add(point)
    session.commit()

    yield point

    session.query(ShortOperationPoint).delete()
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


@pytest.fixture
def strategy(strategy_data, money_management_strategy, indicator, session):
    strategy = Strategy(
        **strategy_data,
        money_management_strategy_id=money_management_strategy.id,
        indicator_id=indicator.id,
    )

    session.add(strategy)
    session.commit()

    yield strategy

    session.query(Strategy).delete()
    session.commit()


def test_create_point(short_operation_point, strategy, session):
    point = ShortOperationPointStrategy(
        short_operation_point_id=short_operation_point.id,
        strategy_id=strategy.id,
    )

    session.add(point)
    session.commit()

    assert point.id
    assert point.short_operation_point_id == short_operation_point.id
    assert point.strategy_id == strategy.id

    session.delete(point)
    session.commit()
