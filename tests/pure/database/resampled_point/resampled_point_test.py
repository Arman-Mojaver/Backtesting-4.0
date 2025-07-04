import pytest

from database.models import ResampledPointD1
from fixtures.price_data import get_resampled_d1_data
from utils.date_utils import string_to_datetime


@pytest.fixture
def resampled_point_data():
    return get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-08-21"),
    )[0]


@pytest.fixture
def resampled_point(resampled_point_data):
    return ResampledPointD1(id=4000, **resampled_point_data)


def test_to_request_format(resampled_point, resampled_point_data):
    assert resampled_point.to_request_format() == {
        "id": resampled_point.id,
        "instrument": resampled_point_data["instrument"],
        "open": resampled_point_data["open"],
        "high": resampled_point_data["high"],
        "low": resampled_point_data["low"],
        "close": resampled_point_data["close"],
        "volume": resampled_point_data["volume"],
        "timestamp": resampled_point_data["timestamp"],
    }
