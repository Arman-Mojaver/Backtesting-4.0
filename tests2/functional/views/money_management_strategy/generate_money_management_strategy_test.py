import pytest
from pydantic import ValidationError

from utils.range_utils import InvalidRangeInputsError
from views.money_management_strategy.create_multiple_view import (
    MoneyManagementStrategyGenerator,
)


@pytest.mark.parametrize("type", ["invalid_type", 123])
def tests_invalid_type(type):  # noqa: A002
    with pytest.raises(ValidationError):
        MoneyManagementStrategyGenerator(
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
        MoneyManagementStrategyGenerator(
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
        MoneyManagementStrategyGenerator(
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
        MoneyManagementStrategyGenerator(
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
        MoneyManagementStrategyGenerator(
            type="atr",
            tp_multiplier_range=(1.0, 1.2),
            sl_multiplier_range=(1.0, 1.2),
            atr_parameter_range=(14, 16),
            risk_percentage_range=(start, stop),
        ).run()


def test_generate_multiple(
    money_management_strategies_data,
    money_management_strategy_schemas,
):
    result = MoneyManagementStrategyGenerator(
        type="atr",
        tp_multiplier_range=(1.5, 1.6),
        sl_multiplier_range=(1.0, 1.1),
        atr_parameter_range=(14, 15),
        risk_percentage_range=(2, 3),
    ).run()

    assert result == money_management_strategy_schemas
