import pytest

from database.models import (
    Indicator,
    LongOperationPoint,
    LongOperationPointStrategy,
    MoneyManagementStrategy,
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
def long_operation_point_data():
    return {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
    }


@pytest.fixture
def long_operation_point(long_operation_point_data, money_management_strategy, session):
    point = LongOperationPoint(
        **long_operation_point_data,
        money_management_strategy_id=money_management_strategy.id,
    )

    session.add(point)
    session.commit()

    yield point

    session.query(LongOperationPoint).delete()
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
        "min_annual_roi": 0.09,
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


def test_create_point(long_operation_point, strategy, session):
    point = LongOperationPointStrategy(
        long_operation_point_id=long_operation_point.id,
        strategy_id=strategy.id,
    )

    session.add(point)
    session.commit()

    assert point.id
    assert point.long_operation_point_id == long_operation_point.id
    assert point.strategy_id == strategy.id

    session.delete(point)
    session.commit()


@pytest.fixture
def long_operation_point_strategy_point(long_operation_point, strategy, session):
    point = LongOperationPointStrategy(
        long_operation_point_id=long_operation_point.id,
        strategy_id=strategy.id,
    )

    session.add(point)
    session.commit()

    yield point

    session.query(LongOperationPointStrategy).delete()
    session.commit()


def test_strategies_relationship(
    long_operation_point,
    long_operation_point_strategy_point,
    strategy,
    session,
):
    assert long_operation_point.strategies == [strategy]


def test_long_operation_points_relationship(
    long_operation_point,
    long_operation_point_strategy_point,
    strategy,
    session,
):
    assert strategy.long_operation_points == [long_operation_point]


def test_deleting_strategy_deletes_relationship(
    long_operation_point,
    long_operation_point_strategy_point,
    strategy,
    session,
):
    session.delete(strategy)

    assert long_operation_point.strategies == []
    assert long_operation_point


def test_deleting_long_operation_point_deletes_relationship(
    long_operation_point,
    long_operation_point_strategy_point,
    strategy,
    session,
):
    session.delete(long_operation_point)

    assert strategy.long_operation_points == []
    assert strategy


def test_deleting_long_operation_point_strategy_deletes_relationships(
    long_operation_point,
    long_operation_point_strategy_point,
    strategy,
    session,
):
    session.delete(long_operation_point_strategy_point)

    assert strategy
    assert long_operation_point

    assert strategy.long_operation_points == []
    assert long_operation_point.strategies == []
