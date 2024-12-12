import pytest

from database.models import MoneyManagementStrategy
from testing_utils.dict_utils import lists_are_equal


@pytest.fixture
def points(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
        "identifier": "atr-1.5-1.0-14",
    }

    money_management_strategy_data_2 = {
        "type": "atr",
        "tp_multiplier": 1.7,
        "sl_multiplier": 0.8,
        "parameters": {"atr_parameter": 15},
        "identifier": "atr-1.7-0.8-15",
    }

    point_1 = MoneyManagementStrategy(**money_management_strategy_data_1)
    point_2 = MoneyManagementStrategy(**money_management_strategy_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(MoneyManagementStrategy.query.all(), points)
