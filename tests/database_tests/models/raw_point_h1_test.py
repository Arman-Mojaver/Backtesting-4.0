import pytest
from sqlalchemy.exc import IntegrityError

from database.models import RawPointH1


def test_instrument_datetime_unique_constraint(raw_point_h1_data, session):
    point_1 = RawPointH1(**raw_point_h1_data)
    point_2 = RawPointH1(**raw_point_h1_data)

    session.add_all([point_1, point_2])

    with pytest.raises(IntegrityError):
        session.commit()
