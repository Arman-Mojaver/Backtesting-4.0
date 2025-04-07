import pytest

from database.models import MoneyManagementStrategy, ResampledPointD1
from database.models.resasmpled_point_d1 import HighLowOrder
from fixtures.helpers import generate_identifier
from fixtures.price_data import get_resampled_d1_data
from utils.date_utils import string_to_datetime


# TODO: session can not be removed here because # noqa: TD002, TD003, FIX002
#  the tests check explicitly for the id, and if there is not commit,
#  there is no id (its value is None).
#  Remove the need for checking the id, by refactoring production and test code
@pytest.fixture
def money_management_strategies(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
        "risk": 0.02,
    }
    money_management_strategy_data_2 = {
        "type": "atr",
        "tp_multiplier": 0.6,
        "sl_multiplier": 0.3,
        "parameters": {"atr_parameter": 3},
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
    money_management_strategies = [
        money_management_strategy_1,
        money_management_strategy_2,
    ]

    session.add_all(money_management_strategies)
    session.commit()

    yield money_management_strategies

    session.query(MoneyManagementStrategy).delete()
    session.commit()


@pytest.fixture
def generate_resampled_points():
    def _generate_points(points_data):
        points = []
        for point_data in points_data:
            point = ResampledPointD1(**point_data)
            point.datetime = string_to_datetime(point_data["datetime"]).date()
            point.high_low_order = HighLowOrder(point_data["high_low_order"])
            points.append(point)

        return points

    return _generate_points


@pytest.fixture
def three_resampled_points_d1(generate_resampled_points):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-23"),
    )

    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def three_resampled_points_d1_two_instruments(generate_resampled_points):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-23"),
    )

    points_data_usdcad = get_resampled_d1_data(
        instrument="USDCAD",
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-15"),
    )

    return generate_resampled_points(points_data_eurusd + points_data_usdcad)
