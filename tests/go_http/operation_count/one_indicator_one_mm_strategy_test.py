import json

import pytest
import requests

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
)
from utils.date_utils import datetime_to_string

INSTRUMENT = "EURUSD"


def parse_response(response):
    return json.loads(response.content.decode())


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
        "identifier": "atr-1.5-1.0-14",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy(money_management_strategy_data, session):
    point = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(point)
    session.commit()

    yield point

    session.query(LongOperationPoint).delete()
    session.query(ShortOperationPoint).delete()
    session.delete(point)
    session.commit()


@pytest.fixture
def long_operation_point(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2024-01-01",
        "result": 51,
        "tp": 51,
        "sl": 46,
        "long_balance": [-12, -1, -6, -15, 53],
        "risk": 0.02,
    }

    point = LongOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)


@pytest.fixture
def short_operation_point(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2025-01-01",
        "result": -70,
        "tp": 67,
        "sl": 70,
        "short_balance": [-18, 2, -72],
        "risk": 0.02,
    }

    point = ShortOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)


@pytest.fixture
def short_operation_point_2(money_management_strategy, session):
    point_data = {
        "instrument": "EURUSD",
        "datetime": "2026-01-01",
        "result": 52,
        "tp": 52,
        "sl": 66,
        "short_balance": [-6, 11, 14, -7, 61],
        "risk": 0.02,
    }

    point = ShortOperationPoint(
        money_management_strategy_id=money_management_strategy.id,
        **point_data,
    )
    session.add(point)
    session.commit()

    yield point

    session.delete(point)


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
