import pytest

from database.models import RawPointD1, RawPointH1
from testing_utils.dict_utils import (
    lists_are_equal,
)


@pytest.fixture
def raw_point_d1(raw_point_d1_data, session):
    point = RawPointD1(**raw_point_d1_data)

    session.add(point)
    session.commit()

    yield point

    session.delete(point)
    session.commit()


@pytest.fixture
def points(raw_point_d1, raw_points_h1_data, session):
    point_data_1, point_data_2 = raw_points_h1_data

    point_1 = RawPointH1(raw_point_d1_id=raw_point_d1.id, **point_data_1)
    point_2 = RawPointH1(raw_point_d1_id=raw_point_d1.id, **point_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(RawPointH1.query.all(), points)
