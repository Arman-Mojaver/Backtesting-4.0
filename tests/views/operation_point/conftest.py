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
    money_management_strategy_data = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
    }

    money_management_strategy_1 = MoneyManagementStrategy(
        **money_management_strategy_data,
        identifier=generate_identifier(money_management_strategy_data),
    )

    session.add(money_management_strategy_1)
    session.commit()

    yield money_management_strategy_1

    session.query(MoneyManagementStrategy).delete()
    session.commit()


@pytest.fixture
def money_management_strategies(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
    }
    money_management_strategy_data_2 = {
        "type": "atr",
        "tp_multiplier": 0.6,
        "sl_multiplier": 0.3,
        "parameters": {"atr_parameter": 3},
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


@pytest.fixture
def four_resampled_points_d1_low_atr(generate_resampled_points, session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-23"),
    )
    eurusd_2023_08_23_data = points_data_eurusd[-1]
    eurusd_2023_08_24_data = {
        "datetime": "2023-08-24",
        "instrument": "EURUSD",
        "open": eurusd_2023_08_23_data["close"],
        "high": eurusd_2023_08_23_data["close"] + 0.0005,
        "low": eurusd_2023_08_23_data["close"] - 0.0005,
        "close": eurusd_2023_08_23_data["close"],
        "volume": 60671,
        "high_low_order": "high_first",
    }
    points_data_eurusd.append(eurusd_2023_08_24_data)

    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def five_resampled_points_d1_long_asymmetric_overflow(generate_resampled_points, session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-24"),
    )
    eurusd_2023_08_24_data = points_data_eurusd[-1]
    eurusd_2023_08_25_data = {
        "datetime": "2023-08-25",
        "instrument": "EURUSD",
        "open": eurusd_2023_08_24_data["close"],
        "high": eurusd_2023_08_24_data["close"] + 0.0020,
        "low": eurusd_2023_08_24_data["close"] - 0.0010,
        "close": eurusd_2023_08_24_data["close"],
        "volume": 60671,
        "high_low_order": "high_first",
    }
    points_data_eurusd.append(eurusd_2023_08_25_data)

    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def five_resampled_points_d1_short_asymmetric_overflow(
    generate_resampled_points,
    session,
):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-24"),
    )
    eurusd_2023_08_24_data = points_data_eurusd[-1]
    eurusd_2023_08_25_data = {
        "datetime": "2023-08-25",
        "instrument": "EURUSD",
        "open": eurusd_2023_08_24_data["close"],
        "high": eurusd_2023_08_24_data["close"] - 0.0020,
        "low": eurusd_2023_08_24_data["close"] + 0.0010,
        "close": eurusd_2023_08_24_data["close"],
        "volume": 60671,
        "high_low_order": "high_first",
    }
    points_data_eurusd.append(eurusd_2023_08_25_data)

    return generate_resampled_points(points_data_eurusd)
