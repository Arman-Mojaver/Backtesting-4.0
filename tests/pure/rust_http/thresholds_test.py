import pytest
import requests

from models.signals import SignalGroup
from testing_utils.http_utils import parse_response


@pytest.mark.parametrize(
    ("indicator_values", "high_threshold", "low_threshold", "expected_signal_group"),
    [
        ([], 1.0, -1.0, SignalGroup(long_signals=[], short_signals=[])),
        (
            [
                {"timestamp": 1700006400, "value": 0.5},
                {"timestamp": 1700092800, "value": 0.7},
            ],
            1.0,
            -1.0,
            SignalGroup([], []),
        ),
        (
            [
                {"timestamp": 1703808000, "value": 3.0},
                {"timestamp": 1703894400, "value": 3.1},
            ],
            2.0,
            -1.0,
            SignalGroup([], []),
        ),
        (
            [
                {"timestamp": 1703980800, "value": -2.5},
                {"timestamp": 1704067200, "value": -2.0},
            ],
            1.0,
            -1.0,
            SignalGroup([], []),
        ),
        (
            [
                {"timestamp": 1701043200, "value": -2.0},
                {"timestamp": 1701129600, "value": -1.5},
                {"timestamp": 1701388800, "value": -1.9},
            ],
            1.0,
            -1.5,
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1701216000, "value": -1.0},
                {"timestamp": 1701302400, "value": -2.0},
                {"timestamp": 1701388800, "value": -1.2},
            ],
            1.0,
            -2.0,
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1701216000, "value": 2.5},
                {"timestamp": 1701302400, "value": 2.0},
                {"timestamp": 1701388800, "value": 2.2},
            ],
            2.0,
            -1.0,
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1701216000, "value": 1.0},
                {"timestamp": 1701302400, "value": 1.5},
                {"timestamp": 1701388800, "value": 1.2},
            ],
            1.5,
            -1.0,
            SignalGroup(long_signals=[], short_signals=[]),
        ),
        (
            [
                {"timestamp": 1700006400, "value": -2.0},
                {"timestamp": 1700092800, "value": 0.2},  # long
            ],
            1.5,
            -1.0,
            SignalGroup([1700092800], []),
        ),
        (
            [
                {"timestamp": 1700179200, "value": 2.5},
                {"timestamp": 1700265600, "value": 1.0},  # short
            ],
            2.0,
            -1.5,
            SignalGroup([], [1700265600]),
        ),
        (
            [
                {"timestamp": 1700352000, "value": -3.0},
                {"timestamp": 1700438400, "value": 0.0},  # long
                {"timestamp": 1700524800, "value": -2.5},
                {"timestamp": 1700611200, "value": -0.2},  # long
            ],
            2.0,
            -1.0,
            SignalGroup([1700438400, 1700611200], []),
        ),
        (
            [
                {"timestamp": 1700697600, "value": 3.5},
                {"timestamp": 1700784000, "value": 1.8},  # short
                {"timestamp": 1700870400, "value": 3.0},
                {"timestamp": 1700956800, "value": 1.4},  # short
            ],
            2.5,
            -2.0,
            SignalGroup([], [1700784000, 1700956800]),
        ),
        (
            [
                {"timestamp": 1701043200, "value": -2.5},
                {"timestamp": 1701129600, "value": 0.1},  # long
                {"timestamp": 1701216000, "value": 2.8},
                {"timestamp": 1701302400, "value": 1.5},  # short
            ],
            2.0,
            -1.0,
            SignalGroup([1701129600], [1701302400]),
        ),
        (
            [
                {"timestamp": 1702080000, "value": -2.5},
                {"timestamp": 1702166400, "value": 0.5},  # long
                {"timestamp": 1702252800, "value": 3.2},
                {"timestamp": 1702339200, "value": 1.4},  # short
                {"timestamp": 1702425600, "value": -2.2},
                {"timestamp": 1702512000, "value": 0.3},  # long
            ],
            2.5,
            -1.0,
            SignalGroup([1702166400, 1702512000], [1702339200]),
        ),
        (
            [
                {"timestamp": 1702598400, "value": 2.8},
                {"timestamp": 1702684800, "value": 1.7},  # short
                {"timestamp": 1702771200, "value": -2.0},
                {"timestamp": 1702857600, "value": 0.1},  # long
                {"timestamp": 1702944000, "value": 3.0},
                {"timestamp": 1703030400, "value": 1.9},  # short
            ],
            2.5,
            -1.5,
            SignalGroup([1702857600], [1702684800, 1703030400]),
        ),
        (
            [
                {"timestamp": 1703116800, "value": -3.0},
                {"timestamp": 1703203200, "value": 0.1},  # long
                {"timestamp": 1703289600, "value": -3.1},
                {"timestamp": 1703376000, "value": 0.2},  # long
                {"timestamp": 1703462400, "value": 3.0},
                {"timestamp": 1703548800, "value": 1.7},  # short
                {"timestamp": 1703635200, "value": 2.9},
                {"timestamp": 1703721600, "value": 1.5},  # short
            ],
            2.5,
            -1.0,
            SignalGroup([1703203200, 1703376000], [1703548800, 1703721600]),
        ),
    ],
)
def test_thresholds(
    indicator_values,
    high_threshold,
    low_threshold,
    expected_signal_group,
    rust_endpoint,
):
    data = {
        "indicator_value_list": indicator_values,
        "high_threshold": high_threshold,
        "low_threshold": low_threshold,
    }
    response = requests.post(url=rust_endpoint("thresholds_test"), json=data, timeout=5)
    content = parse_response(response)

    assert SignalGroup(**content.get("data")) == expected_signal_group
