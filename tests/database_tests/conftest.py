import pytest

from config import config  # type: ignore[attr-defined]
from fixtures.price_data import get_points_data
from utils.date_utils import string_to_datetime
from utils.enums import TimeFrame


@pytest.fixture
def raw_point_d1_data():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-13"),
    )[0]


@pytest.fixture
def raw_point_h1_data():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-13"),
    )[0]


@pytest.fixture
def raw_points_h1_data():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime(
            "2023-11-13 00:00:00",
            format=config.DATETIME_FORMAT,
        ),
        to_date=string_to_datetime(
            "2023-11-13 01:00:00",
            format=config.DATETIME_FORMAT,
        ),
    )
