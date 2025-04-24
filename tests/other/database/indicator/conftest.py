import pytest

from database.models import Indicator


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.query(Indicator).delete()
    session.commit()


@pytest.fixture
def other_indicators(indicator_data, indicator_data_2, session):
    indicator_1 = Indicator(**indicator_data)
    indicator_2 = Indicator(**indicator_data_2)

    indicators = [indicator_1, indicator_2]

    session.add_all(indicators)
    session.commit()

    yield indicators

    session.query(Indicator).delete()
