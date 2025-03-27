import requests

from testing_utils.http_utils import parse_response
from utils.date_utils import datetime_to_string

INSTRUMENT = "EURUSD"


# 1 Year


def test_annual_operation_count_with_long_and_short(
    long_operation_point,
    short_operation_point,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point.datetime
                    ): short_operation_point.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [datetime_to_string(long_operation_point.datetime)],
                "short_signals": [datetime_to_string(short_operation_point.datetime)],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 2.0
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


def test_annual_operation_count_with_long(
    long_operation_point,
    short_operation_point,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point.datetime
                    ): short_operation_point.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [datetime_to_string(long_operation_point.datetime)],
                "short_signals": [],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 1.0
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


def test_annual_operation_count_with_short(
    long_operation_point,
    short_operation_point,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point.datetime
                    ): short_operation_point.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [],
                "short_signals": [datetime_to_string(short_operation_point.datetime)],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 1.0
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


# 2 Years


def test_annual_operation_count_with_long_and_short_2(
    long_operation_point,
    short_operation_point_2,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point_2.datetime
                    ): short_operation_point_2.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [datetime_to_string(long_operation_point.datetime)],
                "short_signals": [datetime_to_string(short_operation_point_2.datetime)],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point_2.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 1.0
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


def test_annual_operation_count_with_long_2(
    long_operation_point,
    short_operation_point_2,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point_2.datetime
                    ): short_operation_point_2.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [datetime_to_string(long_operation_point.datetime)],
                "short_signals": [],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point_2.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 0.5
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


def test_annual_operation_count_with_short_2(
    long_operation_point,
    short_operation_point_2,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point_2.datetime
                    ): short_operation_point_2.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [],
                "short_signals": [datetime_to_string(short_operation_point_2.datetime)],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point_2.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 0.5
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


# Partial Operation Point selection
def test_annual_operation_count_with_partial_operation_point_selection_1(  # noqa: PLR0913
    long_operation_point,
    long_operation_point_2,
    short_operation_point,
    short_operation_point_2,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                    datetime_to_string(
                        long_operation_point_2.datetime
                    ): long_operation_point_2.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point.datetime
                    ): short_operation_point.to_request_format(),
                    datetime_to_string(
                        short_operation_point_2.datetime
                    ): short_operation_point_2.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [
                    datetime_to_string(long_operation_point.datetime),
                    datetime_to_string(long_operation_point_2.datetime),
                ],
                "short_signals": [datetime_to_string(short_operation_point.datetime)],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point_2.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 1.5
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


def test_annual_operation_count_with_partial_operation_point_selection_2(  # noqa: PLR0913
    long_operation_point,
    long_operation_point_2,
    short_operation_point,
    short_operation_point_2,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                    datetime_to_string(
                        long_operation_point_2.datetime
                    ): long_operation_point_2.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point.datetime
                    ): short_operation_point.to_request_format(),
                    datetime_to_string(
                        short_operation_point_2.datetime
                    ): short_operation_point_2.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [datetime_to_string(long_operation_point.datetime)],
                "short_signals": [
                    datetime_to_string(short_operation_point.datetime),
                    datetime_to_string(short_operation_point_2.datetime),
                ],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point_2.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 1.5
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20


def test_annual_operation_count_with_partial_operation_point_selection_3(  # noqa: PLR0913
    long_operation_point,
    long_operation_point_2,
    short_operation_point,
    short_operation_point_2,
    endpoint,
    session,
):
    body = {
        "operation_points": {
            10: {  # money_management_strategy_id
                "long_operation_points": {
                    datetime_to_string(
                        long_operation_point.datetime
                    ): long_operation_point.to_request_format(),
                    datetime_to_string(
                        long_operation_point_2.datetime
                    ): long_operation_point_2.to_request_format(),
                },
                "short_operation_points": {
                    datetime_to_string(
                        short_operation_point.datetime
                    ): short_operation_point.to_request_format(),
                    datetime_to_string(
                        short_operation_point_2.datetime
                    ): short_operation_point_2.to_request_format(),
                },
            },
        },
        "signals": {
            20: {  # indicator_id
                "long_signals": [
                    datetime_to_string(long_operation_point.datetime),
                    datetime_to_string(long_operation_point_2.datetime),
                ],
                "short_signals": [
                    datetime_to_string(short_operation_point.datetime),
                    datetime_to_string(short_operation_point_2.datetime),
                ],
            },
        },
        "start_date": datetime_to_string(long_operation_point.datetime),
        "end_date": datetime_to_string(short_operation_point_2.datetime),
    }

    response = requests.post(
        url=endpoint("process_strategies"),
        json=body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert len(response_content["data"]) == 1
    assert response_content["data"][0]["strategy_data"]["annual_operation_count"] == 2.0
    assert (
        response_content["data"][0]["strategy_data"]["money_management_strategy_id"] == 10
    )
    assert response_content["data"][0]["strategy_data"]["indicator_id"] == 20
