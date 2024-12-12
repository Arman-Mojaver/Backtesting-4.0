import pytest

from database.models.money_management_strategy import MoneyManagementStrategy


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
    }


def test_create_point(money_management_strategy_data, session):
    point = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(point)
    session.commit()

    assert point.id
    assert point.to_dict() == money_management_strategy_data

    session.delete(point)
    session.commit()


@pytest.fixture
def money_management_strategy_point(money_management_strategy_data, session):
    point = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(point)
    session.commit()

    return point


def test_delete_point(money_management_strategy_point, session):
    money_management_strategy_id = money_management_strategy_point.id

    money_management_strategy_point.delete()
    session.commit()

    assert (
        not session.query(MoneyManagementStrategy)
        .filter_by(id=money_management_strategy_id)
        .one_or_none()
    )
