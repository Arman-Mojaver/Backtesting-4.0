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

    return indicators


@pytest.fixture
def other_indicators_rsi(session):
    indicator_data_1 = {
        "type": "rsi",
        "parameters": {"n": 14},
        "identifier": "rsi.n-14",
    }
    indicator_data_2 = {
        "type": "rsi",
        "parameters": {"n": 15},
        "identifier": "rsi.n-15",
    }

    indicator_1 = Indicator(**indicator_data_1)
    indicator_2 = Indicator(**indicator_data_2)

    indicators = [indicator_1, indicator_2]

    session.add_all(indicators)
    session.commit()

    return indicators
