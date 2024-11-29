import pytest

from schemas.raw_points_schema import RawPointsSchema


@pytest.fixture
def raw_points_schema_data(file_data):
    return file_data["data"]["EURUSD"]


def test_valid_raw_points_schema(raw_points_schema_data):
    raw_points_data = RawPointsSchema(**raw_points_schema_data)

    assert raw_points_data.model_dump() == raw_points_schema_data
