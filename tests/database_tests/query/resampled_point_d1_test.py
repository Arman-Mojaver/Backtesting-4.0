import pytest

from database.models import ResampledPointD1
from testing_utils.dict_utils import lists_are_equal


@pytest.fixture
def points(session):
    point_data_1 = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
        "high_low_order": "high_first",
    }

    point_data_2 = {
        "datetime": "2023-11-14",
        "instrument": "EURUSD",
        "open": 1.06916,
        "high": 1.08872,
        "low": 1.06916,
        "close": 1.08782,
        "volume": 79728,
        "high_low_order": "low_first",
    }

    point_1 = ResampledPointD1(**point_data_1)
    point_2 = ResampledPointD1(**point_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(ResampledPointD1.query.all(), points)
