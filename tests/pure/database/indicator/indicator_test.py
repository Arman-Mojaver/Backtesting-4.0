import pytest

from database.models.indicator import Indicator


@pytest.fixture
def indicator_point(indicator_data):
    return Indicator(**indicator_data)


def test_to_dict_with_ids(indicator_point):
    result = indicator_point.to_dict_with_ids()
    assert indicator_point.id == result["id"]
