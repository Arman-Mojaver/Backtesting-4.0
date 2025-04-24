import pytest
from sqlalchemy import delete

from database.models import (
    Indicator,
    LongOperationPoint,
    MoneyManagementStrategy,
    Strategy,
)
from testing_utils.strategy_utils.random_data_generator import (
    generate_random_strategy_data,
)


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.execute(delete(Strategy))
    session.execute(delete(LongOperationPoint))
    session.execute(delete(MoneyManagementStrategy))
    session.execute(delete(Indicator))
    session.commit()


@pytest.fixture
def indicator_data_3():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 14, "price_target": "close"},
            "fast": {"type": "ema", "n": 6, "price_target": "close"},
        },
        "identifier": "macd.sma-14-close,ema-6-close",
    }


@pytest.fixture
def indicator(indicator_data):
    return Indicator(id=10, **indicator_data)


@pytest.fixture
def indicator_2(indicator_data_2):
    return Indicator(id=11, **indicator_data_2)


@pytest.fixture
def indicator_3(indicator_data_3):
    return Indicator(id=12, **indicator_data_3)


@pytest.fixture
def money_management_strategy_data_3():
    return {
        "type": "atr",
        "tp_multiplier": 3.7,
        "sl_multiplier": 3.8,
        "parameters": {"atr_parameter": 15},
        "identifier": "atr-3.7-3.8-15",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy_3(money_management_strategy_data_3):
    return MoneyManagementStrategy(id=3, **money_management_strategy_data_3)


@pytest.fixture
def strategies_data():
    return [generate_random_strategy_data() for _ in range(1)]


@pytest.fixture
def strategies(
    strategies_data,
    indicator_3,
    money_management_strategy_3,
):
    items = [Strategy(**item) for item in strategies_data]
    items[0].money_management_strategy = money_management_strategy_3
    items[0].indicator = indicator_3

    return items


@pytest.fixture
def other_strategies_data():
    return [generate_random_strategy_data() for _ in range(4)]


@pytest.fixture
def other_strategies(  # noqa: PLR0913
    other_strategies_data,
    indicator,
    indicator_2,
    money_management_strategy,
    money_management_strategy_2,
    session,
):
    items = [Strategy(**item) for item in other_strategies_data]
    items[0].money_management_strategy = money_management_strategy
    items[1].money_management_strategy = money_management_strategy
    items[2].money_management_strategy = money_management_strategy_2
    items[3].money_management_strategy = money_management_strategy_2

    items[0].indicator = indicator
    items[1].indicator = indicator_2
    items[2].indicator = indicator
    items[3].indicator = indicator_2

    session.add_all(items)
    session.commit()

    return items


@pytest.fixture
def other_long_operation_points(money_management_strategy, session):
    point_data_1 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-26",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.04,
    }

    point_data_2 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-27",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.04,
    }

    point_1 = LongOperationPoint(
        **point_data_1,
        money_management_strategy_id=money_management_strategy.id,
    )

    point_2 = LongOperationPoint(
        **point_data_2,
        money_management_strategy_id=money_management_strategy.id,
    )

    points = [point_1, point_2]

    session.add(money_management_strategy)
    session.add_all(points)
    session.commit()

    return points


@pytest.fixture
def strategy_with_long_operation_points(
    money_management_strategy,
    indicator,
    other_long_operation_points,
    session,
):
    strategy_data = generate_random_strategy_data()
    strategy = Strategy(**strategy_data)
    strategy.money_management_strategy = money_management_strategy
    strategy.indicator = indicator

    long_op_1, _ = other_long_operation_points
    strategy.long_operation_points.append(long_op_1)

    session.add(strategy)
    session.commit()

    return strategy
