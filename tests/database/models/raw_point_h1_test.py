import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.models import RawPointD1, RawPointH1


@pytest.fixture
def raw_point_d1(session):
    point_data = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point = RawPointD1(**point_data)

    session.add(point)
    session.commit()

    yield point

    session.delete(point)
    session.commit()


def test_create_point(raw_point_d1, session):
    point_data = {
        "datetime": "2023-11-13 00:00:00",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point = RawPointH1(raw_point_d1_id=raw_point_d1.id, **point_data)

    session.add(point)
    session.commit()

    assert point.id
    assert point.to_dict() == point_data

    session.delete(point)
    session.commit()


def test_instrument_datetime_unique_constraint(session):
    point_data_1 = {
        "datetime": "2023-11-13 00:00:00",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point_data_2 = {
        "datetime": "2023-11-13 00:00:00",
        "instrument": "EURUSD",
        "open": 1.06916,
        "high": 1.08872,
        "low": 1.06916,
        "close": 1.08782,
        "volume": 79728,
    }

    point_1 = RawPointH1(**point_data_1)
    point_2 = RawPointH1(**point_data_2)

    session.add_all([point_1, point_2])

    with pytest.raises(IntegrityError):
        session.commit()


def test_raw_point_h1_foreign_key_when_there_is_no_raw_point_d1(session):
    raw_point_h1_data = {
        "datetime": "2023-11-13 00:00:00",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point = RawPointH1(**raw_point_h1_data)

    session.add(point)

    with pytest.raises(SQLAlchemyError):
        session.commit()


def test_relationships(raw_point_d1, session):
    point_data = {
        "datetime": "2023-11-13 00:00:00",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point = RawPointH1(raw_point_d1_id=raw_point_d1.id, **point_data)

    session.add(point)
    session.commit()

    assert point.raw_point_d1.to_dict() == raw_point_d1.to_dict()
    assert raw_point_d1.raw_points_h1[0].to_dict() == point.to_dict()

    session.delete(point)
    session.commit()
