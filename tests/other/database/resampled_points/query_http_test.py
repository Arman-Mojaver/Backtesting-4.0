import requests

from testing_utils.http_utils import parse_response

NON_EXISTENT_INSTRUMENT = "NON_EXISTENT"


def test_empty_table(rust_endpoint, session):
    data = {"instrument": NON_EXISTENT_INSTRUMENT}

    response = requests.post(
        url=rust_endpoint("query_resampled_points_by_instrument"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_unmatched_items(other_resampled_points_usdcad, rust_endpoint, session):
    data = {"instrument": NON_EXISTENT_INSTRUMENT}

    response = requests.post(
        url=rust_endpoint("query_resampled_points_by_instrument"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_only_matched_items(
    other_resampled_points_usdcad,
    rust_endpoint,
    session,
):
    point_1, *_ = other_resampled_points_usdcad

    data = {"instrument": point_1.instrument}

    response = requests.post(
        url=rust_endpoint("query_resampled_points_by_instrument"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    expected_result = [
        item.to_dict(rules=("id", "-datetime", "-high_low_order"))
        for item in other_resampled_points_usdcad
    ]

    assert content["data"] == expected_result


def test_table_has_matched_and_unmatched_items(
    resampled_points,
    other_resampled_points_usdcad,
    rust_endpoint,
    session,
):
    session.add_all(resampled_points)
    session.commit()

    point_1, *_ = resampled_points

    data = {"instrument": point_1.instrument}

    response = requests.post(
        url=rust_endpoint("query_resampled_points_by_instrument"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    expected_result = [
        item.to_dict(rules=("id", "-datetime", "-high_low_order"))
        for item in resampled_points
    ]

    assert content["data"] == expected_result
