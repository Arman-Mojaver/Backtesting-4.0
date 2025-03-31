import pytest

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ResampledPointD1,
    ShortOperationPoint,
)
from fixtures.helpers import generate_identifier
from fixtures.price_data import get_resampled_d1_data
from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)
from utils.date_utils import string_to_datetime


@pytest.fixture
def delete_operation_points(session):
    yield
    session.query(LongOperationPoint).delete()
    session.query(ShortOperationPoint).delete()
    session.commit()


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
def three_resampled_points_d1_two_instruments(generate_resampled_points, session):
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


@pytest.fixture
def generate_long_operation_points(session):
    def _generate_long_operation_points(
        money_management_strategy_id,
        instrument,
        start_date,
        count,
    ):
        points = generate_random_long_operation_points(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            start_date=start_date,
            count=count,
        )

        session.add_all(points)
        session.commit()

        return points

    yield _generate_long_operation_points

    session.query(LongOperationPoint).delete()
    session.commit()


@pytest.fixture
def generate_short_operation_points(session):
    def _generate_short_operation_points(
        money_management_strategy_id,
        instrument,
        start_date,
        count,
    ):
        points = generate_random_short_operation_points(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            start_date=start_date,
            count=count,
        )

        session.add_all(points)
        session.commit()

        return points

    yield _generate_short_operation_points

    session.query(ShortOperationPoint).delete()
    session.commit()
