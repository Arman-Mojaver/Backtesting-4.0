from database.models import ResampledPointD1
from testing_utils.set_utils import set_of_tuples


def test_all_empty():
    assert ResampledPointD1.query.all() == []


def test_all(other_resampled_points):
    assert set_of_tuples(ResampledPointD1.query.all()) == set_of_tuples(
        other_resampled_points
    )


def test_from_instrument_empty():
    assert ResampledPointD1.query.from_instrument("EURUSD").all() == []


def test_from_instrument_non_existent_instrument(other_resampled_points):
    assert ResampledPointD1.query.from_instrument("NON_EXISTENT_INSTRUMENT").all() == []


def test_from_instrument(other_resampled_points):
    eurusd_item, usdcad_item = other_resampled_points
    assert set_of_tuples(
        ResampledPointD1.query.from_instrument("EURUSD").all()
    ) == set_of_tuples([eurusd_item])
    assert set_of_tuples(
        ResampledPointD1.query.from_instrument("USDCAD").all()
    ), set_of_tuples([usdcad_item])
