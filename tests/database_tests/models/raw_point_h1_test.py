import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.models import RawPointD1, RawPointH1


@pytest.fixture
def raw_point_d1(raw_point_d1_data, session):
    point = RawPointD1(**raw_point_d1_data)

    session.add(point)
    session.commit()

    yield point

    session.delete(point)
    session.commit()


def test_create_point(raw_point_d1, raw_point_h1_data, session):
    point = RawPointH1(raw_point_d1_id=raw_point_d1.id, **raw_point_h1_data)

    session.add(point)
    session.commit()

    assert point.id
    assert point.to_dict() == raw_point_h1_data

    session.delete(point)
    session.commit()


def test_instrument_datetime_unique_constraint(raw_point_h1_data, session):
    point_1 = RawPointH1(**raw_point_h1_data)
    point_2 = RawPointH1(**raw_point_h1_data)

    session.add_all([point_1, point_2])

    with pytest.raises(IntegrityError):
        session.commit()


def test_raw_point_h1_foreign_key_when_there_is_no_raw_point_d1(
    raw_point_h1_data,
    session,
):
    point = RawPointH1(**raw_point_h1_data)

    session.add(point)

    with pytest.raises(SQLAlchemyError):
        session.commit()


def test_relationships(raw_point_d1, raw_point_h1_data, session):
    point = RawPointH1(raw_point_d1_id=raw_point_d1.id, **raw_point_h1_data)

    session.add(point)
    session.commit()

    assert point.raw_point_d1.to_dict() == raw_point_d1.to_dict()
    assert raw_point_d1.raw_points_h1[0].to_dict() == point.to_dict()

    session.delete(point)
    session.commit()
