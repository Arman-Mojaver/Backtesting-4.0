from unittest.mock import patch

import pytest

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
)
from fixtures.helpers import generate_identifier
from testing_utils.dict_utils import list_of_dicts_are_equal
from views.operation_points_view import OperationPointsCreateMultipleView


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("three_resampled_points_d1")
def test_create_one_pair_without_balance_overflow(
    money_management_strategy,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    assert len(long_operation_points) == 1
    assert len(short_operation_points) == 1

    long_operation_point = long_operation_points[0]
    short_operation_point = session.query(ShortOperationPoint).all()[0]

    assert (
        long_operation_point.money_management_strategy_id == money_management_strategy.id
    )
    assert (
        short_operation_point.money_management_strategy_id == money_management_strategy.id
    )

    assert long_operation_point.to_dict() == {
        "instrument": "EURUSD",
        "datetime": "2023-08-23",
        "result": -14,
        "tp": 29,
        "sl": 14,
        "long_balance": [
            int(round(10000 * (-1.08448 + 1.08715))),  #  27
            int(round(10000 * (-1.08448 + 1.08026))),  # -42
        ],
    }

    assert short_operation_point.to_dict() == {
        "instrument": "EURUSD",
        "datetime": "2023-08-23",
        "result": -14,
        "tp": 29,
        "sl": 14,
        "short_balance": [
            -int(round(10000 * (-1.08448 + 1.08715))),  # -27
            -int(round(10000 * (-1.08448 + 1.08026))),  #  42
        ],
    }


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("four_resampled_points_d1")
def test_create_two_pairs_without_balance_overflow(
    money_management_strategy,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [
                int(round(10000 * (-1.08448 + 1.08715))),  #  27
                int(round(10000 * (-1.08448 + 1.08026))),  # -42
                int(round(10000 * (-1.08448 + 1.08767))),  #  32
                int(round(10000 * (-1.08448 + 1.0805))),  # -40
            ],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [
                int(round(10000 * (-1.08631 + 1.08767))),  #  14
                int(round(10000 * (-1.08631 + 1.0805))),  # -58
            ],
        },
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [
                -int(round(10000 * (-1.08448 + 1.08715))),  # -27
                -int(round(10000 * (-1.08448 + 1.08026))),  #  42
                -int(round(10000 * (-1.08448 + 1.08767))),  # -32
                -int(round(10000 * (-1.08448 + 1.0805))),  #  40
            ],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [
                -int(round(10000 * (-1.08631 + 1.08767))),  # -14
                -int(round(10000 * (-1.08631 + 1.0805))),  #  58
            ],
        },
    ]

    assert (
        i.money_management_strategy_id == money_management_strategy.id
        for i in long_operation_points
    )
    assert (
        i.money_management_strategy_id == money_management_strategy.id
        for i in short_operation_points
    )
    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


@pytest.fixture
def money_management_strategy_with_large_multipliers(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 500,
        "sl_multiplier": 500,
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


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("four_resampled_points_d1")
def test_do_not_create_with_balance_overflow(
    money_management_strategy_with_large_multipliers,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    assert session.query(LongOperationPoint).all() == []
    assert session.query(ShortOperationPoint).all() == []


@pytest.fixture
def money_management_strategy_with_symmetric_balance_overflow(session):
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


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("four_resampled_points_d1_low_atr")
def test_create_with_symmetric_balance_overflow(
    money_management_strategy_with_symmetric_balance_overflow,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42, 23, 13],
        }
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [-27, 42, -23, -13],
        }
    ]

    assert (
        i.money_management_strategy_id
        == money_management_strategy_with_symmetric_balance_overflow.id
        for i in long_operation_points
    )
    assert (
        i.money_management_strategy_id
        == money_management_strategy_with_symmetric_balance_overflow.id
        for i in short_operation_points
    )
    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("five_resampled_points_d1_long_asymmetric_overflow")
def test_create_with_long_asymmetric_balance_overflow(
    money_management_strategy_with_symmetric_balance_overflow,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42, 32, -40, -15, -45],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [14, -58, -34, -64],
        },
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [-27, 42, -32, 40, 15, 45],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [-14, 58, 34, 64],
        },
    ]

    assert (
        i.money_management_strategy_id
        == money_management_strategy_with_symmetric_balance_overflow.id
        for i in long_operation_points
    )
    assert (
        i.money_management_strategy_id
        == money_management_strategy_with_symmetric_balance_overflow.id
        for i in short_operation_points
    )
    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("five_resampled_points_d1_short_asymmetric_overflow")
def test_create_with_short_asymmetric_balance_overflow(
    money_management_strategy_with_symmetric_balance_overflow,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42, 32, -40, -55, -25],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [14, -58, -74, -44],
        },
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [-27, 42, -32, 40, 55, 25],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [-14, 58, 74, 44],
        },
    ]

    assert (
        i.money_management_strategy_id
        == money_management_strategy_with_symmetric_balance_overflow.id
        for i in long_operation_points
    )
    assert (
        i.money_management_strategy_id
        == money_management_strategy_with_symmetric_balance_overflow.id
        for i in short_operation_points
    )
    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)
