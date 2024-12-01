from unittest.mock import patch

import pytest
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database.models import RawPointD1, RawPointH1
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from testing_utils.dict_utils import list_of_dicts_are_equal
from views.raw_points_view import RawPointsCreateMultipleView


def test_no_file_raises_error():
    with pytest.raises(FileNotFoundError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def _setup_ignored_file(generate_file, file_data):
    generate_file(filename="random.json", data=file_data)


@pytest.mark.usefixtures("_setup_ignored_file")
def test_file_with_wrong_name_raises_error():
    with pytest.raises(FileNotFoundError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def file_data_with_extra_raw_points_d1_field(file_data):
    file_data["data"]["EURUSD"]["raw_points_d1"][0]["extra_key"] = "extra_value"
    return file_data


@pytest.fixture
def _setup_file_with_extra_raw_points_d1_field(
    generate_file,
    file_data_with_extra_raw_points_d1_field,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_extra_raw_points_d1_field,
    )


@pytest.mark.usefixtures("_setup_file_with_mismatched_instruments")
def test_extra_raw_points_d1_fields_return_error():
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def file_data_with_extra_raw_points_h1_field(file_data):
    file_data["data"]["EURUSD"]["raw_points_h1"][0]["extra_key"] = "extra_value"
    return file_data


@pytest.fixture
def _setup_file_with_extra_raw_points_h1_field(
    generate_file,
    file_data_with_extra_raw_points_h1_field,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_extra_raw_points_h1_field,
    )


@pytest.mark.usefixtures("_setup_file_with_extra_raw_points_h1_field")
def test_extra_raw_points_h1_fields_return_error():
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def file_data_with_mismatched_instruments(file_data):
    file_data["data"]["EURUSD"]["raw_points_d1"][0]["instrument"] = "USDCAD"
    return file_data


@pytest.fixture
def _setup_file_with_mismatched_instruments(
    generate_file,
    file_data_with_mismatched_instruments,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_mismatched_instruments,
    )


@pytest.mark.usefixtures("_setup_file_with_mismatched_instruments")
def test_mismatches_between_instruments_raises_error():
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def file_data_with_extra_h1_data(file_data):
    # D1: keep first day, remove second day. H1: keep both days
    file_data["data"]["EURUSD"]["raw_points_d1"] = file_data["data"]["EURUSD"][
        "raw_points_d1"
    ][0:1]
    return file_data


@pytest.fixture
def _setup_file_with_extra_h1_data(
    generate_file,
    file_data_with_extra_h1_data,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_extra_h1_data,
    )


@pytest.mark.usefixtures("_setup_file_with_extra_h1_data")
def test_extra_h1_data_raises_error():
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def file_data_with_extra_d1_data(file_data):
    # D1: keep both days . H1: keep first day, remove second day
    file_data["data"]["EURUSD"]["raw_points_h1"] = file_data["data"]["EURUSD"][
        "raw_points_h1"
    ][0:2]
    return file_data


@pytest.fixture
def _setup_file_with_extra_d1_data(
    generate_file,
    file_data_with_extra_d1_data,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_extra_d1_data,
    )


@pytest.mark.usefixtures("_setup_file_with_extra_d1_data")
def test_extra_d1_data_raises_error():
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView().run()


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


@pytest.fixture
def _setup_file_with_mismatched_end_dates(
    generate_file,
    file_data_with_mismatched_end_dates,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_mismatched_end_dates,
    )


@pytest.mark.usefixtures("_setup_file_with_mismatched_end_dates")
def test_file_data_with_mismatched_end_dates_raises_error():
    with pytest.raises(ValidationError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def file_data_with_less_instruments_than_enabled(file_data):
    file_data["data"].pop("USDCAD")
    return file_data


@pytest.fixture
def _setup_file_with_less_instruments_than_enabled(
    generate_file,
    file_data_with_less_instruments_than_enabled,
):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data_with_less_instruments_than_enabled,
    )


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
@pytest.mark.usefixtures("_setup_file_with_less_instruments_than_enabled")
def test_mismatch_with_less_instruments_than_enabled_raises_error():
    with pytest.raises(EnabledInstrumentsMismatchError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def _setup_file_with_more_instruments_than_enabled(generate_file, file_data):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data,
    )


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("_setup_file_with_more_instruments_than_enabled")
def test_mismatch_with_more_instruments_than_enabled_raises_error():
    with pytest.raises(EnabledInstrumentsMismatchError):
        RawPointsCreateMultipleView().run()


@pytest.fixture
def _setup_file_data(generate_file, file_data):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data,
    )


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
@pytest.mark.usefixtures("_setup_file_data")
def test_create_raw_points(file_data):
    RawPointsCreateMultipleView().run()

    raw_points_d1 = [point.to_dict() for point in RawPointD1.query.all()]
    expected_raw_point_d1_data = [
        point_data
        for instrument in file_data["data"].values()
        for point_data in instrument["raw_points_d1"]
    ]

    raw_points_h1 = [point.to_dict() for point in RawPointH1.query.all()]
    expected_raw_point_h1_data = [
        point_data
        for instrument in file_data["data"].values()
        for point_data in instrument["raw_points_h1"]
    ]

    assert list_of_dicts_are_equal(raw_points_d1, expected_raw_point_d1_data)
    assert list_of_dicts_are_equal(raw_points_h1, expected_raw_point_h1_data)


@patch("views.raw_points_view.session")
@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
@pytest.mark.usefixtures("_setup_file_data")
def test_commit_error(mock_session):
    mock_session.commit.side_effect = SQLAlchemyError

    RawPointsCreateMultipleView().run()

    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
