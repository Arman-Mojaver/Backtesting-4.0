import pytest

from database.models import ResampledPointD1
from database.models.resampled_point_d1 import HighLowOrder
from fixtures.price_data import get_resampled_d1_data
from utils.date_utils import string_to_datetime


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
def resampled_points_d1(generate_resampled_points):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-29"),
    )
    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def three_resampled_points_d1(generate_resampled_points):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-23"),
    )

    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def four_resampled_points_d1(generate_resampled_points):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-24"),
    )

    return generate_resampled_points(points_data_eurusd)


@pytest.fixture
def four_resampled_points_d1_low_atr(generate_resampled_points):
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
def five_resampled_points_d1_long_asymmetric_overflow(generate_resampled_points):
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
