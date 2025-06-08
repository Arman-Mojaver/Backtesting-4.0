import pytest
import requests

from database.models import Indicator, ResampledPointD1
from database.models.resampled_point_d1 import ResampledPointD1List
from fixtures.indicator_data import get_indicator_data
from fixtures.price_data import get_resampled_d1_data
from testing_utils.http_utils import parse_response
from testing_utils.models import IndicatorValue
from utils.date_utils import string_to_datetime


@pytest.mark.parametrize("rsi_n_value", [3, 4])
@pytest.mark.parametrize("instrument", ["EURUSD", "USDCAD", "AUDUSD", "AUDCAD"])
def test_rsi(rsi_n_value, instrument, rust_endpoint):
    resampled_points_data = get_resampled_d1_data(
        instrument,
        string_to_datetime("2023-11-13"),
        string_to_datetime("2023-11-27"),
    )

    resampled_points = []
    for index, point_data in enumerate(resampled_points_data, 1):
        point = ResampledPointD1(**point_data)
        point.id = index
        resampled_points.append(point)

    indicator = Indicator(
        id=234,
        type="rsi",
        parameters={"n": rsi_n_value},
        identifier=f"rsi.n{rsi_n_value}",
    )

    data = {
        "resampled_points": ResampledPointD1List(resampled_points).to_request_format(),
        "indicator": indicator.to_request_format(),
    }

    response = requests.post(
        url=rust_endpoint("rsi_test"),
        json=data,
        timeout=5,
    )

    expected_result_data = get_indicator_data(
        indicator="rsi",
        instrument=instrument,
        params=f"n{rsi_n_value}",
        buffer="b0",
    )
    expected_items = [IndicatorValue(**item) for item in expected_result_data]

    content = parse_response(response)
    items = [IndicatorValue(**item) for item in content["data"]["OneThreshold"]["items"]]

    assert items == expected_items
    assert content["data"]["OneThreshold"]["high_threshold"] == 70.0
    assert content["data"]["OneThreshold"]["low_threshold"] == 30.0
