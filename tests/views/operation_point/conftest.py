import pytest

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ResampledPointD1,
    ShortOperationPoint,
)
from fixtures.helpers import generate_identifier
from fixtures.price_data import get_resampled_d1_data
from utils.date_utils import string_to_datetime


@pytest.fixture
def delete_operation_points(session):
    yield
    session.query(LongOperationPoint).delete()
    session.query(ShortOperationPoint).delete()
    session.commit()


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
def generate_resampled_points(session):
    def _generate_points(points_data):
        points = []
        for point_data in points_data:
            point = ResampledPointD1(**point_data)
            points.append(point)

        session.add_all(points)
        session.commit()

    yield _generate_points

    session.query(ResampledPointD1).delete()
    session.commit()


@pytest.fixture
def resampled_points_d1(generate_resampled_points, session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-29"),
    )
    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def three_resampled_points_d1(generate_resampled_points, session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-23"),
    )

    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def four_resampled_points_d1(generate_resampled_points, session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-24"),
    )

    return generate_resampled_points(points_data_eurusd)
