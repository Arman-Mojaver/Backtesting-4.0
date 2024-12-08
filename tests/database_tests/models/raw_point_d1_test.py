import pytest
from sqlalchemy.exc import IntegrityError

from database.models.raw_point_d1 import RawPointD1


def test_create_point(raw_point_d1_data, session):
    point = RawPointD1(**raw_point_d1_data)

    session.add(point)
    session.commit()

    assert point.id
    assert point.to_dict() == raw_point_d1_data

    session.delete(point)
    session.commit()


def test_instrument_datetime_unique_constraint(raw_point_d1_data, session):
    point_1 = RawPointD1(**raw_point_d1_data)
    point_2 = RawPointD1(**raw_point_d1_data)

    session.add_all([point_1, point_2])

    with pytest.raises(IntegrityError):
        session.commit()
