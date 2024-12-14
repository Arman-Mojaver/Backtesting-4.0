import pytest

from utils.range_utils import InvalidRangeInputsError, frange


@pytest.mark.parametrize(
    ("start", "stop", "step", "expected"),
    [
        (1.1, 1.2, 0.1, [1.1]),
        (1.5, 5.5, 1.5, [1.5, 3.0, 4.5]),
        (1.1, 2.2, 0.2, [1.1, 1.3, 1.5, 1.7, 1.9, 2.1]),
        (1.0, 2.0, 0.333, [1, 1.333, 1.666, 1.999]),

        # start is less than stop
        (5.5, 2.5, 0.1, []),

        # start equals stop
        (5, 5, 1, []),
        (5.5, 5.5, 0.1, []),
    ],
)
def test_frange(start, stop, step, expected):
    assert list(frange(start, stop, step)) == expected


@pytest.mark.parametrize(
    ("start", "stop", "step"),
    [
        # range values have 0
        (0, 5.5, 1.1),
        (1.1, 0, 0.1),
        (1.1, 2.5, 0),
        # range values have negative numbers
        (-2.1, 5.5, 1.1),
        (1.1, -3.5, 0.1),
        (1.1, 2.5, -0.1),
    ],
)
def test_frange_errors(start, stop, step):
    with pytest.raises(InvalidRangeInputsError):
        list(frange(start, stop, step))
