import pytest

from database.models import ResampledPointD1
from database.models.resasmpled_point_d1 import ResampledPointD1List
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
def resampled_point_data_2():
    return get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-22"),
        to_date=string_to_datetime("2023-08-22"),
    )[0]


@pytest.fixture
def resampled_point(resampled_point_data):
    return ResampledPointD1(id=4000, **resampled_point_data)


@pytest.fixture
def resampled_point_2(resampled_point_data_2):
    return ResampledPointD1(id=4001, **resampled_point_data_2)


def test_to_request_data(
    resampled_point, resampled_point_2, resampled_point_data, resampled_point_data_2
):
    assert ResampledPointD1List(
        [resampled_point, resampled_point_2]
    ).to_request_data() == [
        {"id": resampled_point.id, **resampled_point_data},
        {"id": resampled_point_2.id, **resampled_point_data_2},
    ]
