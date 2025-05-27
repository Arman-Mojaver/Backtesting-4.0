import pytest
import requests

from models.signals import SignalGroup
from testing_utils.http_utils import parse_response


@pytest.mark.parametrize(
    ("indicator_values", "expected_signal_group"),
    [
        ([], SignalGroup(long_signals=[], short_signals=[])),
        (
            [{"timestamp": 1704067200, "value": 1.2}],  # 2024-01-01
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [{"timestamp": 1704153600, "value": -1.5}],  # 2024-01-02
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704758400, "value": 1.5},  # 2024-01-09
                {"timestamp": 1704844800, "value": 2.3},  # 2024-01-10
            ],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704931200, "value": -0.6},  # 2024-01-11
                {"timestamp": 1705017600, "value": -1.2},  # 2024-01-12
            ],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704240000, "value": -2.0},  # 2024-01-03
                {"timestamp": 1704326400, "value": 2.0},  # 2024-01-04
            ],
            SignalGroup(long_signals=[1704326400], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704412800, "value": 0.7},  # 2024-01-05
                {"timestamp": 1704672000, "value": -0.9},  # 2024-01-08
            ],
            SignalGroup(long_signals=[], short_signals=[1704672000]),
        ),
        (
            [
                {"timestamp": 1705276800, "value": -1.1},  # 2024-01-15
                {"timestamp": 1705363200, "value": 1.0},  # 2024-01-16
                {"timestamp": 1705449600, "value": 0.5},  # 2024-01-17
            ],
            SignalGroup(long_signals=[1705363200], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1705536000, "value": -0.4},  # 2024-01-18
                {"timestamp": 1705622400, "value": 0.3},  # 2024-01-19
                {"timestamp": 1705881600, "value": -0.8},  # 2024-01-22
                {"timestamp": 1705968000, "value": 0.9},  # 2024-01-23
            ],
            SignalGroup(
                long_signals=[1705622400, 1705968000], short_signals=[1705881600]
            ),
        ),
        (
            [
                {"timestamp": 1706054400, "value": 0.6},  # 2024-01-24
                {"timestamp": 1706140800, "value": 1.2},  # 2024-01-25
                {"timestamp": 1706227200, "value": -1.4},  # 2024-01-26
                {"timestamp": 1706486400, "value": 0.5},  # 2024-01-29
            ],
            SignalGroup(long_signals=[1706486400], short_signals=[1706227200]),
        ),
        (
            [
                {"timestamp": 1706572800, "value": -2.2},  # 2024-01-30
                {"timestamp": 1706659200, "value": -1.1},  # 2024-01-31
                {"timestamp": 1706745600, "value": 2.5},  # 2024-02-01
                {"timestamp": 1706832000, "value": 0.4},  # 2024-02-02
            ],
            SignalGroup(long_signals=[1706745600], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1707091200, "value": 1.1},  # 2024-02-05
                {"timestamp": 1707177600, "value": -1.3},  # 2024-02-06
                {"timestamp": 1707264000, "value": 1.6},  # 2024-02-07
                {"timestamp": 1707350400, "value": -1.9},  # 2024-02-08
            ],
            SignalGroup(
                long_signals=[1707264000], short_signals=[1707177600, 1707350400]
            ),
        ),
        (
            [
                {"timestamp": 1707436800, "value": 2.0},  # 2024-02-09
                {"timestamp": 1707696000, "value": 1.8},  # 2024-02-12
                {"timestamp": 1707782400, "value": -0.5},  # 2024-02-13
                {"timestamp": 1707868800, "value": -0.2},  # 2024-02-14
            ],
            SignalGroup(long_signals=[], short_signals=[1707782400]),
        ),
        (
            [
                {"timestamp": 1707955200, "value": -1.7},  # 2024-02-15
                {"timestamp": 1708041600, "value": 1.9},  # 2024-02-16
                {"timestamp": 1708300800, "value": -0.6},  # 2024-02-19
                {"timestamp": 1708387200, "value": 0.7},  # 2024-02-20
            ],
            SignalGroup(
                long_signals=[1708041600, 1708387200], short_signals=[1708300800]
            ),
        ),
        (
            [
                {"timestamp": 1708473600, "value": 1.2},  # 2024-02-21
                {"timestamp": 1708560000, "value": -1.2},  # 2024-02-22
                {"timestamp": 1708646400, "value": -0.9},  # 2024-02-23
                {"timestamp": 1708905600, "value": 0.4},  # 2024-02-26
            ],
            SignalGroup(long_signals=[1708905600], short_signals=[1708560000]),
        ),
        (
            [
                {"timestamp": 1708992000, "value": -0.3},  # 2024-02-27
                {"timestamp": 1709078400, "value": 1.5},  # 2024-02-28
                {"timestamp": 1709164800, "value": 0.2},  # 2024-02-29
                {"timestamp": 1709251200, "value": -1.0},  # 2024-03-01
            ],
            SignalGroup(long_signals=[1709078400], short_signals=[1709251200]),
        ),
        (
            [
                {"timestamp": 1709510400, "value": -0.8},  # 2024-03-04
                {"timestamp": 1709596800, "value": 0.9},  # 2024-03-05
                {"timestamp": 1709683200, "value": 1.7},  # 2024-03-06
                {"timestamp": 1709769600, "value": -1.5},  # 2024-03-07
                {"timestamp": 1709856000, "value": 1.4},  # 2024-03-08
            ],
            SignalGroup(
                long_signals=[1709596800, 1709856000], short_signals=[1709769600]
            ),
        ),
        (
            [
                {"timestamp": 1710115200, "value": 0.3},  # 2024-03-11
                {"timestamp": 1710201600, "value": -0.4},  # 2024-03-12
                {"timestamp": 1710288000, "value": 0.5},  # 2024-03-13
                {"timestamp": 1710374400, "value": -0.6},  # 2024-03-14
                {"timestamp": 1710460800, "value": 0.7},  # 2024-03-15
            ],
            SignalGroup(
                long_signals=[1710288000, 1710460800],
                short_signals=[1710201600, 1710374400],
            ),
        ),
        (
            [
                {"timestamp": 1710720000, "value": -1.6},  # 2024-03-18
                {"timestamp": 1710806400, "value": -0.3},  # 2024-03-19
                {"timestamp": 1710892800, "value": 1.1},  # 2024-03-20
                {"timestamp": 1710979200, "value": 0.6},  # 2024-03-21
                {"timestamp": 1711065600, "value": -0.1},  # 2024-03-22
            ],
            SignalGroup(long_signals=[1710892800], short_signals=[1711065600]),
        ),
        (
            [
                {"timestamp": 1711324800, "value": 2.1},  # 2024-03-25
                {"timestamp": 1711411200, "value": -2.1},  # 2024-03-26
                {"timestamp": 1711497600, "value": 2.2},  # 2024-03-27
                {"timestamp": 1711584000, "value": -2.2},  # 2024-03-28
                {"timestamp": 1711670400, "value": 2.3},  # 2024-03-29
            ],
            SignalGroup(
                long_signals=[1711497600, 1711670400],
                short_signals=[1711411200, 1711584000],
            ),
        ),
    ],
)
def test_oscillator(indicator_values, expected_signal_group, rust_endpoint):
    data = {"indicator_value_list": indicator_values}
    response = requests.post(url=rust_endpoint("oscillator_test"), json=data, timeout=5)
    content = parse_response(response)

    assert SignalGroup(**content.get("data")) == expected_signal_group
