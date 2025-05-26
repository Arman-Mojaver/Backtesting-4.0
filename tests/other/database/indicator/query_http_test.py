import requests

from testing_utils.http_utils import parse_response

NON_EXISTENT_TYPE = "NON_EXISTENT"


def test_empty_table(rust_endpoint, session):
    data = {"type_": NON_EXISTENT_TYPE}

    response = requests.post(
        url=rust_endpoint("query_indicators_by_type_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_unmatched_items(other_indicators, rust_endpoint, session):
    data = {"type_": NON_EXISTENT_TYPE}

    response = requests.post(
        url=rust_endpoint("query_indicators_by_type_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_only_matched_items(
    other_indicators,
    rust_endpoint,
    session,
):
    indicator_1, *_ = other_indicators

    data = {"type_": indicator_1.type}

    response = requests.post(
        url=rust_endpoint("query_indicators_by_type_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    expected_result = [item.to_dict(rules=("id",)) for item in other_indicators]

    assert content["data"] == expected_result


def test_table_has_matched_and_unmatched_items(
    other_indicators,
    other_indicators_rsi,
    rust_endpoint,
    session,
):
    indicator_1, *_ = other_indicators

    data = {"type_": indicator_1.type}

    response = requests.post(
        url=rust_endpoint("query_indicators_by_type_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    expected_result = [item.to_dict(rules=("id",)) for item in other_indicators]

    assert content["data"] == expected_result
