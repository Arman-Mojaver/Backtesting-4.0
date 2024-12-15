import pytest

from indicators.sma import get_sma

VALUES = [10, 20, 30, 40, 50, 60]


@pytest.mark.parametrize(
    ("n", "expected_result"),
    [
        (
            2,
            [
                (VALUES[0] + VALUES[1]) / 2,
                (VALUES[1] + VALUES[2]) / 2,
                (VALUES[2] + VALUES[3]) / 2,
                (VALUES[3] + VALUES[4]) / 2,
                (VALUES[4] + VALUES[5]) / 2,
            ],
        ),
        (
            3,
            [
                (VALUES[0] + VALUES[1] + VALUES[2]) / 3,
                (VALUES[1] + VALUES[2] + VALUES[3]) / 3,
                (VALUES[2] + VALUES[3] + VALUES[4]) / 3,
                (VALUES[3] + VALUES[4] + VALUES[5]) / 3,
            ],
        ),
        (
            4,
            [
                (VALUES[0] + VALUES[1] + VALUES[2] + VALUES[3]) / 4,
                (VALUES[1] + VALUES[2] + VALUES[3] + VALUES[4]) / 4,
                (VALUES[2] + VALUES[3] + VALUES[4] + VALUES[5]) / 4,
            ],
        ),
        (
            5,
            [
                (VALUES[0] + VALUES[1] + VALUES[2] + VALUES[3] + VALUES[4]) / 5,
                (VALUES[1] + VALUES[2] + VALUES[3] + VALUES[4] + VALUES[5]) / 5,
            ],
        ),
        (
            6,
            [
                (VALUES[0] + VALUES[1] + VALUES[2] + VALUES[3] + VALUES[4] + VALUES[5])
                / 6,
            ],
        ),
    ],
)
def test_simple_moving_average(n, expected_result):
    assert get_sma(VALUES, n) == expected_result
