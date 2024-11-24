import pytest
from sqlalchemy.exc import IntegrityError

from database.models.raw_point_d1 import RawPointD1


def test_create_point(session):
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

    assert point.id
    assert point.to_dict() == point_data

    session.delete(point)
    session.commit()


def test_instrument_datetime_unique_constraint(session):
    point_data_1 = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point_data_2 = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06916,
        "high": 1.08872,
        "low": 1.06916,
        "close": 1.08782,
        "volume": 79728,
    }

    point_1 = RawPointD1(**point_data_1)
    point_2 = RawPointD1(**point_data_2)

    session.add_all([point_1, point_2])

    with pytest.raises(IntegrityError):
        session.commit()
