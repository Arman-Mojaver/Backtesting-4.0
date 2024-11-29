import pytest
from pydantic import ValidationError

from config import config  # type: ignore[attr-defined]
from schemas.raw_point_h1_schema import RawPointH1Schema
from utils.date_utils import string_to_datetime


def test_valid_schema():
    data = {
        "instrument": "EURUSD",
        "datetime": "2023-11-13 00:00",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    raw_point_h1_data = RawPointH1Schema(**data)

    assert raw_point_h1_data.datetime == string_to_datetime(
        data["datetime"],
        config.DATETIME_FORMAT,
    )
    assert raw_point_h1_data.model_dump() == data


def test_extra_fields_return_error():
    data = {
        "instrument": "EURUSD",
        "datetime": "2023-11-13 00:00",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
        "extra_field": "something",
    }

    with pytest.raises(ValidationError):
        RawPointH1Schema(**data)
