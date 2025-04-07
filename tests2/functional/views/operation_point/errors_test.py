import pytest

from database.models import MoneyManagementStrategy
from exceptions import (
    LargeAtrParameterError,
    NoMoneyManagementStrategiesError,
    NoResampledPointsError,
)
from fixtures.helpers import generate_identifier
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from views.operation_points_view import OperationPointsCreateMultipleView


@pytest.fixture
def money_management_strategy_with_large_atr_parameter():
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 8},
        "risk": 0.02,
    }

    return MoneyManagementStrategy(
        **money_management_strategy_data_1,
        identifier=generate_identifier(money_management_strategy_data_1),
    )


@pytest.fixture
def money_management_strategies_with_large_atr_parameter():
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
        "risk": 0.02,
    }
    money_management_strategy_data_2 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 8},
        "risk": 0.02,
    }

    money_management_strategy_1 = MoneyManagementStrategy(
        **money_management_strategy_data_1,
        identifier=generate_identifier(money_management_strategy_data_1),
    )
    money_management_strategy_2 = MoneyManagementStrategy(
        **money_management_strategy_data_2,
        identifier=generate_identifier(money_management_strategy_data_2),
    )
    return [
        money_management_strategy_1,
        money_management_strategy_2,
    ]


def test_no_resampled_points_raises_error(money_management_strategy):
    with pytest.raises(NoResampledPointsError):
        OperationPointsCreateMultipleView([], [money_management_strategy]).run()


def test_no_money_management_strategies_raises_error(resampled_points_d1):
    with pytest.raises(NoMoneyManagementStrategiesError):
        OperationPointsCreateMultipleView(resampled_points_d1, []).run()


def test_atr_parameter_is_greater_than_resampled_points_count_raises_error(
    resampled_points_d1,
    money_management_strategy_with_large_atr_parameter,
):
    with pytest.raises(LargeAtrParameterError):
        OperationPointsCreateMultipleView(
            resampled_points_d1, [money_management_strategy_with_large_atr_parameter]
        ).run()


def test_one_atr_parameter_is_greater_than_resampled_points_count_raises_error(
    resampled_points_d1,
    money_management_strategies_with_large_atr_parameter,
):
    with pytest.raises(LargeAtrParameterError):
        OperationPointsCreateMultipleView(
            resampled_points_d1,
            money_management_strategies_with_large_atr_parameter,
            ("EURUSD",),
        ).run()


def test_mismatch_with_more_instruments_than_enabled_raises_error(
    resampled_points_d1,
    money_management_strategy,
):
    with pytest.raises(EnabledInstrumentsMismatchError):
        OperationPointsCreateMultipleView(
            resampled_points_d1,
            [money_management_strategy],
            ("EURUSD", "USDCAD"),
        ).run()


def test_mismatch_with_less_instruments_than_enabled_raises_error(
    resampled_points_d1,
    money_management_strategy,
):
    with pytest.raises(EnabledInstrumentsMismatchError):
        OperationPointsCreateMultipleView(
            resampled_points_d1,
            [money_management_strategy],
        ).run()
