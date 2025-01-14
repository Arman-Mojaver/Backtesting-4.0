from unittest.mock import patch

import pytest
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database.models import MoneyManagementStrategy
from utils.range_utils import InvalidRangeInputsError
from views.money_management_strategy.create_multiple_view import (
    MoneyManagementStrategyCreateMultipleView,
)


@pytest.mark.parametrize("type", ["invalid_type", 123])
def tests_invalid_type(type):  # noqa: A002
    with pytest.raises(ValidationError):
        MoneyManagementStrategyCreateMultipleView(
            type="invalid_type",
            tp_multiplier_range=(1.0, 1.2),
            sl_multiplier_range=(1.0, 1.2),
            atr_parameter_range=(14, 16),
            risk_percentage_range=(2, 3),
        ).run()


@pytest.mark.parametrize(
    ("start", "stop"),
    [
        # range values have 0
        (0, 5.5),
        (1.1, 0),
        # range values have negative numbers
        (-2.1, 5.5),
        (1.1, -3.5),
    ],
)
def test_invalid_tp_multiplier_range_inputs(start, stop):
    with pytest.raises(InvalidRangeInputsError):
        MoneyManagementStrategyCreateMultipleView(
            type="atr",
            tp_multiplier_range=(start, stop),
            sl_multiplier_range=(1.0, 1.2),
            atr_parameter_range=(14, 16),
            risk_percentage_range=(2, 3),
        ).run()


@pytest.mark.parametrize(
    ("start", "stop"),
    [
        # range values have 0
        (0, 5.5),
        (1.1, 0),
        # range values have negative numbers
        (-2.1, 5.5),
        (1.1, -3.5),
    ],
)
def test_invalid_sl_multiplier_range_inputs(start, stop):
    with pytest.raises(InvalidRangeInputsError):
        MoneyManagementStrategyCreateMultipleView(
            type="atr",
            tp_multiplier_range=(1.0, 1.2),
            sl_multiplier_range=(start, stop),
            atr_parameter_range=(14, 16),
            risk_percentage_range=(2, 3),
        ).run()


@pytest.mark.parametrize(
    ("start", "stop"),
    [
        # range values have 0
        (0, 5),
        (1, 0),
        # range values have negative numbers
        (-2, 5),
        (1, -3),
    ],
)
def test_invalid_atr_parameter_range_inputs(start, stop):
    with pytest.raises(InvalidRangeInputsError):
        MoneyManagementStrategyCreateMultipleView(
            type="atr",
            tp_multiplier_range=(1.0, 1.2),
            sl_multiplier_range=(1.0, 1.2),
            atr_parameter_range=(start, stop),
            risk_percentage_range=(2, 3),
        ).run()


@pytest.mark.parametrize(
    ("start", "stop"),
    [
        # range values have 0
        (0, 5),
        (1, 0),
        # range values have negative numbers
        (-2, 5),
        (1, -3),
    ],
)
def test_invalid_risk_percentage_range_inputs(start, stop):
    with pytest.raises(InvalidRangeInputsError):
        MoneyManagementStrategyCreateMultipleView(
            type="atr",
            tp_multiplier_range=(1.0, 1.2),
            sl_multiplier_range=(1.0, 1.2),
            atr_parameter_range=(14, 16),
            risk_percentage_range=(start, stop),
        ).run()


@pytest.fixture
def money_management_strategies_data():
    return [
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
    ]


def test_create_multiple(money_management_strategies_data, session):
    MoneyManagementStrategyCreateMultipleView(
        type="atr",
        tp_multiplier_range=(1.5, 1.6),
        sl_multiplier_range=(1.0, 1.1),
        atr_parameter_range=(14, 15),
        risk_percentage_range=(2, 3),
    ).run()

    money_management_strategies = MoneyManagementStrategy.query.all()

    assert [
        item.to_dict(rules=("-identifier",)) for item in money_management_strategies
    ] == money_management_strategies_data

    session.query(MoneyManagementStrategy).delete()
    session.commit()


@patch("views.money_management_strategy.create_multiple_view.session")
def test_commit_error(mock_session, money_management_strategies_data):
    mock_session.commit.side_effect = SQLAlchemyError

    with pytest.raises(SQLAlchemyError):
        MoneyManagementStrategyCreateMultipleView(
            type="atr",
            tp_multiplier_range=(1.5, 1.6),
            sl_multiplier_range=(1.0, 1.1),
            atr_parameter_range=(14, 15),
            risk_percentage_range=(2, 3),
        ).run()
