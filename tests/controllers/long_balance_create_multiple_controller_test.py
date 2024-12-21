from unittest.mock import patch

import pytest

from controllers.long_balance_create_multiple_controller import (
    LongBalanceCreateMultipleController,
)
from database.models.resasmpled_point_d1 import ResampledPointD1
from exceptions import NoResampledPointsError
from fixtures.price_data import get_resampled_d1_data
from models.long_balance_point import LongBalancePoint
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from utils.date_utils import string_to_datetime


def test_no_raw_points_raises_error():
    with pytest.raises(NoResampledPointsError):
        LongBalanceCreateMultipleController().run()


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
        LongBalanceCreateMultipleController().run()


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
def test_return_long_balance(resampled_points_d1):
    result = LongBalanceCreateMultipleController().run()

    expected_result = [
        LongBalancePoint(
            instrument="EURUSD",
            datetime="2023-08-23",
            balance=[
                int(round(10000 * (-1.08448 + 1.08715))),
                int(round(10000 * (-1.08448 + 1.08026))),
                int(round(10000 * (-1.08448 + 1.08767))),
                int(round(10000 * (-1.08448 + 1.0805))),
                int(round(10000 * (-1.08448 + 1.0842))),
                int(round(10000 * (-1.08448 + 1.07656))),
                int(round(10000 * (-1.08448 + 1.07928))),
                int(round(10000 * (-1.08448 + 1.08223))),
                int(round(10000 * (-1.08448 + 1.07822))),
                int(round(10000 * (-1.08448 + 1.0892))),
            ],
        ),
        LongBalancePoint(
            instrument="EURUSD",
            datetime="2023-08-24",
            balance=[
                int(round(10000 * (-1.08631 + 1.08767))),
                int(round(10000 * (-1.08631 + 1.0805))),
                int(round(10000 * (-1.08631 + 1.0842))),
                int(round(10000 * (-1.08631 + 1.07656))),
                int(round(10000 * (-1.08631 + 1.07928))),
                int(round(10000 * (-1.08631 + 1.08223))),
                int(round(10000 * (-1.08631 + 1.07822))),
                int(round(10000 * (-1.08631 + 1.0892))),
            ],
        ),
        LongBalancePoint(
            instrument="EURUSD",
            datetime="2023-08-25",
            balance=[
                int(round(10000 * (-1.08086 + 1.0842))),
                int(round(10000 * (-1.08086 + 1.07656))),
                int(round(10000 * (-1.08086 + 1.07928))),
                int(round(10000 * (-1.08086 + 1.08223))),
                int(round(10000 * (-1.08086 + 1.07822))),
                int(round(10000 * (-1.08086 + 1.0892))),
            ],
        ),
        LongBalancePoint(
            instrument="EURUSD",
            datetime="2023-08-28",
            balance=[
                int(round(10000 * (-1.07958 + 1.07928))),
                int(round(10000 * (-1.07958 + 1.08223))),
                int(round(10000 * (-1.07958 + 1.07822))),
                int(round(10000 * (-1.07958 + 1.0892))),
            ],
        ),
        LongBalancePoint(
            instrument="EURUSD",
            datetime="2023-08-29",
            balance=[
                int(round(10000 * (-1.08186 + 1.07822))),
                int(round(10000 * (-1.08186 + 1.0892))),
            ],
        ),
        LongBalancePoint(
            instrument="USDCAD",
            datetime="2023-11-13",
            balance=[
                int(round(10000 * (-1.37935 + 1.38314))),
                int(round(10000 * (-1.37935 + 1.37767))),
                int(round(10000 * (-1.37935 + 1.38429))),
                int(round(10000 * (-1.37935 + 1.36842))),
                int(round(10000 * (-1.37935 + 1.37094))),
                int(round(10000 * (-1.37935 + 1.36543))),
            ],
        ),
        LongBalancePoint(
            instrument="USDCAD",
            datetime="2023-11-14",
            balance=[
                int(round(10000 * (-1.38011 + 1.38429))),
                int(round(10000 * (-1.38011 + 1.36842))),
                int(round(10000 * (-1.38011 + 1.37094))),
                int(round(10000 * (-1.38011 + 1.36543))),
            ],
        ),
        LongBalancePoint(
            instrument="USDCAD",
            datetime="2023-11-15",
            balance=[
                int(round(10000 * (-1.36833 + 1.37094))),
                int(round(10000 * (-1.36833 + 1.36543))),
            ],
        ),
    ]

    assert result == expected_result
