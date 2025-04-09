import pytest
from sqlalchemy.exc import IntegrityError

from database.models import Indicator


def test_unique_identifier(indicator_data_1, session):
    indicator_1 = Indicator(**indicator_data_1)
    indicator_2 = Indicator(**indicator_data_1)

    session.add_all([indicator_1, indicator_2])

    with pytest.raises(IntegrityError):
        session.commit()
