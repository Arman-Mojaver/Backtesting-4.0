import pytest
from sqlalchemy.exc import IntegrityError

from database.models import ResampledPointD1


def test_instrument_datetime_unique_constraint(session):
    point_data = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
        "high_low_order": "high_first",
    }

    point_1 = ResampledPointD1(**point_data)
    point_2 = ResampledPointD1(**point_data)

    session.add_all([point_1, point_2])

    with pytest.raises(IntegrityError):
        session.commit()
