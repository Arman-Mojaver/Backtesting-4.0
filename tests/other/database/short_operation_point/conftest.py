import pytest

from database.models import (
    Indicator,
    MoneyManagementStrategy,
    ShortOperationPoint,
    Strategy,
)
from testing_utils.strategy_utils.random_data_generator import (
    generate_random_strategy_data,
)
from utils.date_utils import string_to_datetime


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.query(ShortOperationPoint).delete()
    session.query(MoneyManagementStrategy).delete()
    session.query(Indicator).delete()
    session.commit()


@pytest.fixture
def money_management_strategy(money_management_strategy_data, session):
    money_management_strategy = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(money_management_strategy)
    session.commit()

    return money_management_strategy


@pytest.fixture
def short_operation_points_data():
    return [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
            "timestamp": int(string_to_datetime("2023-08-24").timestamp()),
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-25",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
            "timestamp": int(string_to_datetime("2023-08-25").timestamp()),
        },
    ]


@pytest.fixture
def short_operation_points(money_management_strategy, short_operation_points_data):
    return [
        ShortOperationPoint(
            **short_operation_point_data,
            money_management_strategy_id=money_management_strategy.id,
        )
        for short_operation_point_data in short_operation_points_data
    ]


@pytest.fixture
def other_short_operation_points(money_management_strategy, session):
    point_data_1 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-26",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.04,
        "timestamp": int(string_to_datetime("2023-08-26").timestamp()),
    }

    point_data_2 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-27",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.04,
        "timestamp": int(string_to_datetime("2023-08-27").timestamp()),
    }

    point_1 = ShortOperationPoint(
        **point_data_1,
        money_management_strategy_id=money_management_strategy.id,
    )

    point_2 = ShortOperationPoint(
        **point_data_2,
        money_management_strategy_id=money_management_strategy.id,
    )

    points = [point_1, point_2]

    session.add_all(points)
    session.commit()

    return points


@pytest.fixture
def indicator(indicator_data):
    return Indicator(id=11, **indicator_data)


@pytest.fixture
def strategy_with_short_operation_points(
    money_management_strategy,
    indicator,
    other_short_operation_points,
    session,
):
    strategy_data = generate_random_strategy_data()
    strategy = Strategy(**strategy_data)
    strategy.money_management_strategy = money_management_strategy
    strategy.indicator = indicator

    short_op_1, _ = other_short_operation_points
    strategy.short_operation_points.append(short_op_1)

    session.add(strategy)
    session.commit()

    return strategy
