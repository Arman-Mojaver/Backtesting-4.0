import pytest
from pydantic import ValidationError

from schemas.instruments_schema import EnabledInstrumentsMismatchError
from views.raw_points.raw_points_view import RawPointsCreateMultipleView


@pytest.fixture
def file_data_with_extra_raw_points_d1_field(file_data):
    file_data["data"]["EURUSD"]["raw_points_d1"][0]["extra_key"] = "extra_value"
    return file_data


def test_extra_raw_points_d1_fields_return_error(
    file_data_with_extra_raw_points_d1_field,
):
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView(file_data_with_extra_raw_points_d1_field).run()


@pytest.fixture
def file_data_with_extra_raw_points_h1_field(file_data):
    file_data["data"]["EURUSD"]["raw_points_h1"][0]["extra_key"] = "extra_value"
    return file_data


def test_extra_raw_points_h1_fields_return_error(
    file_data_with_extra_raw_points_h1_field,
):
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView(file_data_with_extra_raw_points_h1_field).run()


@pytest.fixture
def file_data_with_mismatched_instruments(file_data):
    file_data["data"]["EURUSD"]["raw_points_d1"][0]["instrument"] = "USDCAD"
    return file_data


def test_mismatches_between_instruments_raises_error(
    file_data_with_mismatched_instruments,
):
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView(file_data_with_mismatched_instruments).run()


@pytest.fixture
def file_data_with_extra_h1_data(file_data):
    # D1: keep first day, remove second day. H1: keep both days
    file_data["data"]["EURUSD"]["raw_points_d1"] = file_data["data"]["EURUSD"][
        "raw_points_d1"
    ][0:1]
    return file_data


def test_extra_h1_data_raises_error(file_data_with_extra_h1_data):
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView(file_data_with_extra_h1_data).run()


@pytest.fixture
def file_data_with_extra_d1_data(file_data):
    # D1: keep both days . H1: keep first day, remove second day
    file_data["data"]["EURUSD"]["raw_points_h1"] = file_data["data"]["EURUSD"][
        "raw_points_h1"
    ][0:2]
    return file_data


def test_extra_d1_data_raises_error(file_data_with_extra_d1_data):
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView(file_data_with_extra_d1_data).run()


@pytest.fixture
def file_data_with_mismatched_end_dates(file_data):
    # Last day for USDCAD is 2023-11-13. Last day for EURUSD is 2023-11-14
    file_data["data"]["USDCAD"]["raw_points_d1"] = file_data["data"]["USDCAD"][
        "raw_points_d1"
    ][0:1]
    file_data["data"]["USDCAD"]["raw_points_h1"] = file_data["data"]["USDCAD"][
        "raw_points_h1"
    ][0:2]
    return file_data


def test_file_data_with_mismatched_end_dates_raises_error(
    file_data_with_mismatched_end_dates,
):
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView(file_data_with_mismatched_end_dates).run()


@pytest.fixture
def file_data_with_less_instruments_than_enabled(file_data):
    file_data["data"].pop("USDCAD")
    return file_data


def test_mismatch_with_less_instruments_than_enabled_raises_error(
    file_data_with_less_instruments_than_enabled,
):
    with pytest.raises(EnabledInstrumentsMismatchError):
        RawPointsCreateMultipleView(
            file_data_with_less_instruments_than_enabled, ("EURUSD", "USDCAD")
        ).run()


def test_mismatch_with_more_instruments_than_enabled_raises_error(file_data):
    with pytest.raises(EnabledInstrumentsMismatchError):
        RawPointsCreateMultipleView(file_data, ("EURUSD",)).run()
