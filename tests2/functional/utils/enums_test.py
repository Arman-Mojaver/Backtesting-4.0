import pytest

from utils.enums import TimeFrame


@pytest.mark.parametrize(
    ("enum_type", "value"),
    [
        (TimeFrame.Day, "D1"),
        (TimeFrame.Hour, "H1"),
    ],
    ids=str,
)
def test_time_frame(enum_type, value):
    assert enum_type.value == value
