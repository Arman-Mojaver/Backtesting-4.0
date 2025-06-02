import pytest
import requests

from models.signals import SignalGroup
from testing_utils.http_utils import parse_response

# TODO: What happens if they have the same value,  # noqa: FIX002, TD002, TD003
#  also applicable to oscillator value = 0. Can this be solved with rounding?
"""
# (
#     [
#         {"timestamp": 1706054400, "value": 1.0},
#         {"timestamp": 1706140800, "value": 1.0},
#         {"timestamp": 1706227200, "value": 0.9},
#         {"timestamp": 1706486400, "value": 1.1},
#     ],
#     [
#         {"timestamp": 1706054400, "value": 1.0},
#         {"timestamp": 1706140800, "value": 1.0},
#         {"timestamp": 1706227200, "value": 1.2},
#         {"timestamp": 1706486400, "value": 1.0},
#     ],
#     SignalGroup(
#         long_signals=[1706486400],
#         short_signals=[1706227200],
#     ),
# ),
"""


@pytest.mark.parametrize(
    ("upcross_long_buffer", "upcross_short_buffer", "expected_signal_group"),
    [
        ([], [], SignalGroup(long_signals=[], short_signals=[])),
        (
            [{"timestamp": 1708300800, "value": 1.0}],
            [{"timestamp": 1708300800, "value": 2.0}],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704153600, "value": 2.0},
                {"timestamp": 1704240000, "value": 3.0},
            ],
            [
                {"timestamp": 1704153600, "value": 1.0},
                {"timestamp": 1704240000, "value": 1.5},
            ],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704326400, "value": 0.5},
                {"timestamp": 1704412800, "value": 0.2},
            ],
            [
                {"timestamp": 1704326400, "value": 1.0},
                {"timestamp": 1704412800, "value": 2.0},
            ],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1705881600, "value": 0.5},
                {"timestamp": 1705968000, "value": -0.7},
            ],
            [
                {"timestamp": 1705881600, "value": 0.5},
                {"timestamp": 1705968000, "value": -0.7},
            ],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1712777600, "value": -2.0},
                {"timestamp": 1712864000, "value": -1.5},
            ],
            [
                {"timestamp": 1712777600, "value": -1.0},
                {"timestamp": 1712864000, "value": -0.5},
            ],
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704499200, "value": 0.8},
                {"timestamp": 1704585600, "value": 1.2},
            ],
            [
                {"timestamp": 1704499200, "value": 1.0},
                {"timestamp": 1704585600, "value": 0.9},
            ],
            SignalGroup(long_signals=[1704585600], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1704672000, "value": 1.5},
                {"timestamp": 1704758400, "value": 0.7},
            ],
            [
                {"timestamp": 1704672000, "value": 1.0},
                {"timestamp": 1704758400, "value": 1.2},
            ],
            SignalGroup(long_signals=[], short_signals=[1704758400]),
        ),
        (
            [
                {"timestamp": 1705017600, "value": 0.5},
                {"timestamp": 1705104000, "value": 1.5},
                {"timestamp": 1705190400, "value": 0.8},
            ],
            [
                {"timestamp": 1705017600, "value": 1.0},
                {"timestamp": 1705104000, "value": 1.2},
                {"timestamp": 1705190400, "value": 1.0},
            ],
            SignalGroup(long_signals=[1705104000], short_signals=[1705190400]),
        ),
        (
            [
                {"timestamp": 1705276800, "value": 2.0},
                {"timestamp": 1705363200, "value": 1.0},
                {"timestamp": 1705449600, "value": 1.5},
            ],
            [
                {"timestamp": 1705276800, "value": 1.0},
                {"timestamp": 1705363200, "value": 1.2},
                {"timestamp": 1705449600, "value": -2.0},
            ],
            SignalGroup(long_signals=[1705449600], short_signals=[1705363200]),
        ),
        (
            [
                {"timestamp": 1705536000, "value": 0.0},
                {"timestamp": 1705622400, "value": 2.0},
                {"timestamp": 1705708800, "value": -1.0},
                {"timestamp": 1705795200, "value": 1.0},
            ],
            [
                {"timestamp": 1705536000, "value": 1.0},
                {"timestamp": 1705622400, "value": 1.5},
                {"timestamp": 1705708800, "value": 1.2},
                {"timestamp": 1705795200, "value": 0.5},
            ],
            SignalGroup(
                long_signals=[1705622400, 1705795200],
                short_signals=[1705708800],
            ),
        ),
        (
            [
                {"timestamp": 1712000000, "value": -2.0},
                {"timestamp": 1712086400, "value": 0.5},
            ],
            [
                {"timestamp": 1712000000, "value": -1.0},
                {"timestamp": 1712086400, "value": -0.2},
            ],
            SignalGroup(long_signals=[1712086400], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1712172800, "value": 1.0},
                {"timestamp": 1712259200, "value": -0.7},
            ],
            [
                {"timestamp": 1712172800, "value": 0.5},
                {"timestamp": 1712259200, "value": 0.0},
            ],
            SignalGroup(long_signals=[], short_signals=[1712259200]),
        ),
        (
            [
                {"timestamp": 1712345600, "value": -1.5},
                {"timestamp": 1712432000, "value": -1.1},
            ],
            [
                {"timestamp": 1712345600, "value": -2.0},
                {"timestamp": 1712432000, "value": -1.0},
            ],
            SignalGroup(long_signals=[], short_signals=[1712432000]),
        ),
        (
            [
                {"timestamp": 1712518400, "value": -0.5},
                {"timestamp": 1712604800, "value": -1.2},
            ],
            [
                {"timestamp": 1712518400, "value": -1.0},
                {"timestamp": 1712604800, "value": -0.8},
            ],
            SignalGroup(long_signals=[], short_signals=[1712604800]),
        ),
        (
            [
                {"timestamp": 1713036800, "value": 0.0},
                {"timestamp": 1713123200, "value": 2.0},
                {"timestamp": 1713209600, "value": -1.0},
                {"timestamp": 1713296000, "value": 1.5},
                {"timestamp": 1713382400, "value": -0.5},
            ],
            [
                {"timestamp": 1713036800, "value": 1.0},
                {"timestamp": 1713123200, "value": 1.5},
                {"timestamp": 1713209600, "value": 0.0},
                {"timestamp": 1713296000, "value": 1.0},
                {"timestamp": 1713382400, "value": 0.0},
            ],
            SignalGroup(
                long_signals=[1713123200, 1713296000],
                short_signals=[1713209600, 1713382400],
            ),
        ),
    ],
)
def test_crossover(
    upcross_long_buffer,
    upcross_short_buffer,
    expected_signal_group,
    rust_endpoint,
):
    data = {
        "upcross_long_buffer": upcross_long_buffer,
        "upcross_short_buffer": upcross_short_buffer,
    }
    response = requests.post(url=rust_endpoint("crossover_test"), json=data, timeout=5)
    content = parse_response(response)

    assert SignalGroup(**content.get("data")) == expected_signal_group
