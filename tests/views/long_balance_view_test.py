from unittest.mock import patch

import pytest

from database.models.resasmpled_point_d1 import ResampledPointD1
from fixtures.price_data import get_resampled_d1_data
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from utils.date_utils import string_to_datetime
from views.long_balance_view import LongBalanceView, NoResampledPointsError


def test_no_raw_points_raises_error():
    with pytest.raises(NoResampledPointsError):
        LongBalanceView().run()


@pytest.fixture
def resampled_points_d1(session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-23"),
        to_date=string_to_datetime("2023-08-29"),
    )

    points_data_usdcad = get_resampled_d1_data(
        instrument="USDCAD",
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-15"),
    )

    points = []
    for point_data in [*points_data_eurusd, *points_data_usdcad]:
        point = ResampledPointD1(**point_data)
        points.append(point)

    session.add_all(points)
    session.commit()

    yield points

    for point in points:
        session.delete(point)

    session.commit()


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
def test_raw_points_has_mismatch_with_enabled_instruments(resampled_points_d1):
    with pytest.raises(EnabledInstrumentsMismatchError):
        LongBalanceView().run()


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
def test_return_long_balance(resampled_points_d1):
    result = LongBalanceView().run()

    expected_result = {
        "EURUSD": {
            "2023-08-23": [
                -1.08448 + 1.08715,
                -1.08448 + 1.08026,
                -1.08448 + 1.08767,
                -1.08448 + 1.0805,
                -1.08448 + 1.0842,
                -1.08448 + 1.07656,
                -1.08448 + 1.07928,
                -1.08448 + 1.08223,
                -1.08448 + 1.07822,
                -1.08448 + 1.0892,
            ],
            "2023-08-24": [
                -1.08631 + 1.08767,
                -1.08631 + 1.0805,
                -1.08631 + 1.0842,
                -1.08631 + 1.07656,
                -1.08631 + 1.07928,
                -1.08631 + 1.08223,
                -1.08631 + 1.07822,
                -1.08631 + 1.0892,
            ],
            "2023-08-25": [
                -1.08086 + 1.0842,
                -1.08086 + 1.07656,
                -1.08086 + 1.07928,
                -1.08086 + 1.08223,
                -1.08086 + 1.07822,
                -1.08086 + 1.0892,
            ],
            "2023-08-28": [
                -1.07958 + 1.07928,
                -1.07958 + 1.08223,
                -1.07958 + 1.07822,
                -1.07958 + 1.0892,
            ],
            "2023-08-29": [
                -1.08186 + 1.07822,
                -1.08186 + 1.0892,
            ],
        },
        "USDCAD": {
            "2023-11-13": [
                -1.37935 + 1.38314,
                -1.37935 + 1.37767,
                -1.37935 + 1.38429,
                -1.37935 + 1.36842,
                -1.37935 + 1.37094,
                -1.37935 + 1.36543,
            ],
            "2023-11-14": [
                -1.38011 + 1.38429,
                -1.38011 + 1.36842,
                -1.38011 + 1.37094,
                -1.38011 + 1.36543,
            ],
            "2023-11-15": [
                -1.36833 + 1.37094,
                -1.36833 + 1.36543,
            ],
        },
    }

    assert result == expected_result
