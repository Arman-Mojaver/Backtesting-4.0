import pytest

from database.models import RawPointD1
from fixtures.price_data import get_points_data
from testing_utils.dict_utils import (
    lists_are_equal,
)
from utils.date_utils import string_to_datetime
from utils.enums import TimeFrame


@pytest.fixture
def points(session):
    point_data_1, point_data_2 = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-14"),
    )

    point_1 = RawPointD1(**point_data_1)
    point_2 = RawPointD1(**point_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(RawPointD1.query.all(), points)
