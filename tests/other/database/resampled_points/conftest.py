import pytest

from database.models import ResampledPointD1
from database.models.resasmpled_point_d1 import HighLowOrder
from utils.date_utils import string_to_datetime


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    for item in session.query(ResampledPointD1).all():
        session.delete(item)
    session.commit()


@pytest.fixture
def resampled_point_data_1():
    return {
        "datetime": string_to_datetime("2023-11-13").date(),
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
        "high_low_order": HighLowOrder.high_first,
    }


@pytest.fixture
def resampled_point_data_2():
    return {
        "datetime": string_to_datetime("2023-11-14").date(),
        "instrument": "EURUSD",
        "open": 1.06916,
        "high": 1.08872,
        "low": 1.06916,
        "close": 1.08782,
        "volume": 79728,
        "high_low_order": HighLowOrder.low_first,
    }


@pytest.fixture
def resampled_points(resampled_point_data_1, resampled_point_data_2):
    return [
        ResampledPointD1(**resampled_point_data_1),
        ResampledPointD1(**resampled_point_data_2),
    ]


@pytest.fixture
def other_resampled_points(session):
    point_data_1 = {
        "datetime": string_to_datetime("2023-11-15").date(),
        "instrument": "EURUSD",
        "open": 1.07916,
        "high": 1.09872,
        "low": 1.07916,
        "close": 1.09782,
        "volume": 89728,
        "high_low_order": HighLowOrder.undefined,
    }

    point_data_2 = {
        "datetime": string_to_datetime("2023-11-16").date(),
        "instrument": "EURUSD",
        "open": 1.08916,
        "high": 1.10872,
        "low": 1.08916,
        "close": 1.10782,
        "volume": 99728,
        "high_low_order": HighLowOrder.high_first,
    }

    points = [ResampledPointD1(**point_data_1), ResampledPointD1(**point_data_2)]

    session.add_all(points)
    session.commit()

    return points
