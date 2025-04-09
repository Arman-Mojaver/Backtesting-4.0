import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.max_draw_down import (
    MaxDrawDownRequestBodyFactory,
    StrategyResponseMaxDrawDown,
)
from tests.pure.finance_utils.draw_down_test import DRAW_DOWN_RESULT_MAPPING

INSTRUMENT = "EURUSD"


def test_no_signals_returns_zero(endpoint):
    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-03",
        long_signals=[[]],
        short_signals=[[]],
        long_results=[1, 2, 9],
        long_tps=[1, 2, 9],
        long_sls=[1, 2, 9],
        short_results=[1, 2, 9],
        short_tps=[1, 2, 9],
        short_sls=[1, 2, 9],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == 0.0
    )


def test_all_positives_returns_zero(endpoint):
    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-03",
        long_signals=[["2024-01-01"]],
        short_signals=[["2024-01-02"]],
        long_results=[50, 30, 40],
        long_tps=[50, 30, 40],
        long_sls=[20, 20, 20],
        short_results=[50, 30, 40],
        short_tps=[50, 30, 40],
        short_sls=[20, 20, 20],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == 0.0
    )


def test_all_selected_positives_returns_zero(endpoint):
    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-03",
        long_signals=[["2024-01-01"]],
        short_signals=[["2024-01-02"]],
        long_results=[50, -30, -40],
        long_tps=[50, 25, 45],
        long_sls=[20, 30, 40],
        short_results=[-50, 30, -40],
        short_tps=[60, 30, 65],
        short_sls=[50, 20, 40],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == 0.0
    )


def test_negative_and_positive(endpoint):
    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-03",
        long_signals=[["2024-01-01"]],
        short_signals=[["2024-01-02"]],
        long_results=[-50, -30, -40],
        long_tps=[20, 40, 45],
        long_sls=[50, 30, 40],
        short_results=[-50, 30, -40],
        short_tps=[60, 30, 60],
        short_sls=[50, 20, 40],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == 2.0
    )


def test_two_negatives(endpoint):
    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-03",
        long_signals=[["2024-01-01"]],
        short_signals=[["2024-01-02"]],
        long_results=[-50, -30, -40],
        long_tps=[20, 40, 45],
        long_sls=[50, 30, 40],
        short_results=[-50, -30, -40],
        short_tps=[60, 35, 65],
        short_sls=[50, 30, 40],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == 4.0
    )


def test_positive_and_negative(endpoint):
    parameters = ((30, 30, 20), (-20, 30, 20))
    op_1, op_2 = parameters
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]

    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-02",
        long_signals=[["2024-01-01"]],
        short_signals=[["2024-01-02"]],
        long_results=[op_1[0], 9],
        long_tps=[op_1[1], 9],
        long_sls=[op_1[2], 7],
        short_results=[-7, op_2[0]],
        short_tps=[9, op_2[1]],
        short_sls=[7, op_2[2]],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == expected_result
    )


def test_positive_and_two_negatives(endpoint):
    parameters = ((30, 30, 20), (-20, 30, 20), (-20, 30, 20))
    op_1, op_2, op_3 = parameters
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]

    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-03",
        long_signals=[["2024-01-01", "2024-01-03"]],
        short_signals=[["2024-01-02"]],
        long_results=[op_1[0], 9, op_3[0]],
        long_tps=[op_1[1], 9, op_3[1]],
        long_sls=[op_1[2], 7, op_3[2]],
        short_results=[-7, op_2[0], 9],
        short_tps=[9, op_2[1], 9],
        short_sls=[7, op_2[2], 7],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == expected_result
    )


def test_two_negatives_and_several_positives(endpoint):
    parameters = ((-20, 30, 20), (-20, 30, 20), (30, 30, 20), (30, 30, 20), (30, 30, 20))
    op_1, op_2, op_3, op_4, op_5 = parameters
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]

    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-05",
        long_signals=[["2024-01-01", "2024-01-03", "2024-01-05"]],
        short_signals=[["2024-01-02", "2024-01-04"]],
        long_results=[op_1[0], 9, op_3[0], 9, op_5[0]],
        long_tps=[op_1[1], 9, op_3[1], 9, op_5[1]],
        long_sls=[op_1[2], 7, op_3[2], 7, op_5[2]],
        short_results=[-7, op_2[0], 9, op_4[0], 9],
        short_tps=[9, op_2[1], 9, op_4[1], 9],
        short_sls=[7, op_2[2], 7, op_4[2], 7],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == expected_result
    )


def test_mix_of_positives_and_negatives_1(endpoint):
    parameters = (
        (-20, 30, 20),
        (-20, 30, 20),
        (30, 30, 20),
        (25, 25, 20),
        (-200, 300, 200),
        (300, 300, 250),
    )
    op_1, op_2, op_3, op_4, op_5, op_6 = parameters
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]

    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-08",
        long_signals=[["2024-01-01", "2024-01-03", "2024-01-05"]],
        short_signals=[["2024-01-02", "2024-01-04", "2024-01-08"]],
        long_results=[op_1[0], 9, op_3[0], 9, op_5[0], 9],
        long_tps=[op_1[1], 9, op_3[1], 9, op_5[1], 9],
        long_sls=[op_1[2], 7, op_3[2], 7, op_5[2], 7],
        short_results=[-7, op_2[0], 9, op_4[0], 9, op_6[0]],
        short_tps=[9, op_2[1], 9, op_4[1], 9, op_6[1]],
        short_sls=[7, op_2[2], 7, op_4[2], 7, op_6[2]],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == expected_result
    )


def test_mix_of_positives_and_negatives_2(endpoint):
    parameters = (
        (-20, 30, 20),
        (-20, 30, 20),
        (30, 30, 20),
        (25, 25, 20),
        (-200, 300, 200),
        (-250, 300, 250),
        (-250, 300, 250),
    )
    op_1, op_2, op_3, op_4, op_5, op_6, op_7 = parameters
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]

    request_body = MaxDrawDownRequestBodyFactory(
        instrument=INSTRUMENT,
        mm_strategy_id=1,
        start_date="2024-01-01",
        end_date="2024-01-09",
        long_signals=[["2024-01-01", "2024-01-03", "2024-01-05", "2024-01-09"]],
        short_signals=[["2024-01-02", "2024-01-04", "2024-01-08"]],
        long_results=[op_1[0], 9, op_3[0], 9, op_5[0], 9, op_7[0]],
        long_tps=[op_1[1], 9, op_3[1], 9, op_5[1], 9, op_7[1]],
        long_sls=[op_1[2], 7, op_3[2], 7, op_5[2], 7, op_7[2]],
        short_results=[-7, op_2[0], 9, op_4[0], 9, op_6[0], -7],
        short_tps=[9, op_2[1], 9, op_4[1], 9, op_6[1], 9],
        short_sls=[7, op_2[2], 7, op_4[2], 7, op_6[2], 7],
    )

    response = requests.post(
        url=endpoint("process_strategies"),
        json=request_body.body,
        timeout=5,
    )

    response_content = parse_response(response)

    assert (
        StrategyResponseMaxDrawDown.model_validate(
            response_content["data"][0]
        ).strategy_data.max_draw_down
        == expected_result
    )
