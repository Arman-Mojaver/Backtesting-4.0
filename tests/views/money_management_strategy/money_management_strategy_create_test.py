from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database.models import MoneyManagementStrategy
from views.money_management_strategy.money_management_strategy_create_one_view import (
    MoneyManagementStrategyCreateOneView,
)


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
    }


def test_create_one(money_management_strategy_data, session):
    MoneyManagementStrategyCreateOneView(**money_management_strategy_data).run()

    money_management_strategy = (
        session.query(MoneyManagementStrategy)
        .filter_by(identifier="atr-1.5-1.0-14")
        .one()
    )

    assert (
        money_management_strategy.to_dict(rules=("-identifier",))
        == money_management_strategy_data
    )


@patch(
    "views.money_management_strategy.money_management_strategy_create_one_view.session"
)
def test_commit_error(mock_session, money_management_strategy_data):
    mock_session.commit.side_effect = SQLAlchemyError

    MoneyManagementStrategyCreateOneView(**money_management_strategy_data).run()

    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
