from database.models import ResampledPointD1
from testing_utils.dict_utils import lists_are_equal


def test_all_empty():
    assert ResampledPointD1.query.all() == []


def test_all(other_resampled_points):
    assert lists_are_equal(ResampledPointD1.query.all(), other_resampled_points)


def test_from_instrument_empty():
    assert ResampledPointD1.query.from_instrument("EURUSD").all() == []


def test_from_instrument_non_existent_instrument(other_resampled_points):
    assert ResampledPointD1.query.from_instrument("NON_EXISTENT_INSTRUMENT").all() == []


def test_from_instrument(other_resampled_points):
    eurusd_item, usdcad_item = other_resampled_points
    assert lists_are_equal(
        ResampledPointD1.query.from_instrument("EURUSD").all(), [eurusd_item]
    )
    assert lists_are_equal(
        ResampledPointD1.query.from_instrument("USDCAD").all(), [usdcad_item]
    )
