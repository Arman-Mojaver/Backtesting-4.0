from unittest.mock import patch

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
def money_management_strategy(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
    }

    money_management_strategy_1 = MoneyManagementStrategy(
        **money_management_strategy_data_1,
        identifier=generate_identifier(money_management_strategy_data_1),
    )

    session.add(money_management_strategy_1)
    session.commit()

    yield money_management_strategy_1

    session.query(MoneyManagementStrategy).delete()
    session.commit()


@pytest.fixture
def money_management_strategy_with_large_atr_parameter(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 8},
    }

    money_management_strategy_1 = MoneyManagementStrategy(
        **money_management_strategy_data_1,
        identifier=generate_identifier(money_management_strategy_data_1),
    )

    session.add(money_management_strategy_1)
    session.commit()

    yield money_management_strategy_1

    session.query(MoneyManagementStrategy).delete()
    session.commit()


@pytest.mark.usefixtures("money_management_strategy")
def test_no_resampled_points_raises_error():
    with pytest.raises(NoResampledPointsError):
        OperationPointsCreateMultipleView().run()


@pytest.mark.usefixtures("resampled_points_d1")
def test_no_money_management_strategies_raises_error():
    with pytest.raises(NoMoneyManagementStrategiesError):
        OperationPointsCreateMultipleView().run()


@pytest.mark.usefixtures(
    "resampled_points_d1",
    "money_management_strategy_with_large_atr_parameter",
)
def test_atr_parameter_is_greater_than_resampled_points_count_raises_error():
    with pytest.raises(LargeAtrParameterError):
        OperationPointsCreateMultipleView().run()


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
@pytest.mark.usefixtures("resampled_points_d1", "money_management_strategy")
def test_mismatch_with_more_instruments_than_enabled_raises_error():
    with pytest.raises(EnabledInstrumentsMismatchError):
        OperationPointsCreateMultipleView().run()


@pytest.mark.usefixtures("resampled_points_d1", "money_management_strategy")
def test_mismatch_with_less_instruments_than_enabled_raises_error():
    with pytest.raises(EnabledInstrumentsMismatchError):
        OperationPointsCreateMultipleView().run()
