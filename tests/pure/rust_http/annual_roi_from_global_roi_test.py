import pytest
import requests

from pure.finance_utils.annual_roi_from_global_roi_test import END_DATE_GLOBAL_ROI
from testing_utils.http_utils import parse_response


@pytest.mark.parametrize(("end_date", "global_roi"), END_DATE_GLOBAL_ROI)
def test_calculate_annual_roi(end_date, global_roi, rust_endpoint):
    start_date, expected_result = "2023-01-01", 10.0

    data = {
        "global_roi": global_roi,
        "start_date": start_date,
        "end_date": end_date,
    }

    response = requests.post(
        url=rust_endpoint("annual_roi_from_global_roi"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    assert content["data"] == expected_result
