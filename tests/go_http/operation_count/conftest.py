import pytest

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
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

    session.query(LongOperationPoint).delete()
    session.query(ShortOperationPoint).delete()
    session.delete(point)
    session.commit()


@pytest.fixture
def long_operation_point(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2024-01-01",
        "result": 51,
        "tp": 51,
        "sl": 46,
        "long_balance": [-12, -1, -6, -15, 53],
        "risk": 0.02,
    }

    point = LongOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)


@pytest.fixture
def long_operation_point_2(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2025-07-01",
        "result": 51,
        "tp": 51,
        "sl": 46,
        "long_balance": [-12, -1, -6, -15, 53],
        "risk": 0.02,
    }

    point = LongOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)


@pytest.fixture
def short_operation_point(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2025-01-01",
        "result": -70,
        "tp": 67,
        "sl": 70,
        "short_balance": [-18, 2, -72],
        "risk": 0.02,
    }

    point = ShortOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)


@pytest.fixture
def short_operation_point_2(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2026-01-01",
        "result": 52,
        "tp": 52,
        "sl": 66,
        "short_balance": [-6, 11, 14, -7, 61],
        "risk": 0.02,
    }

    point = ShortOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)
