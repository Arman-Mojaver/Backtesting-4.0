import pytest

from schemas.instruments_schema import InstrumentsSchema


def test_valid_instruments_schema(file_data):
    instruments_data = InstrumentsSchema(**file_data)

    assert instruments_data.model_dump() == file_data


@pytest.fixture
def file_data_with_mismatched_instruments(file_data):
    file_data["data"]["EURUSD"]["raw_points_d1"][0]["instrument"] = "USDCAD"
    return file_data


def test_mismatches_between_instruments_raises_error(
    file_data_with_mismatched_instruments,
):
    with pytest.raises(ValueError):
        InstrumentsSchema(**file_data_with_mismatched_instruments)


@pytest.fixture
def file_data_with_extra_h1_data(file_data):
    # D1: keep first day, remove second day. H1: keep both days
    file_data["data"]["EURUSD"]["raw_points_d1"] = file_data["data"]["EURUSD"][
        "raw_points_d1"
    ][0:1]
    return file_data


def test_extra_h1_data_raises_error(file_data_with_extra_h1_data):
    with pytest.raises(ValueError):
        InstrumentsSchema(**file_data_with_extra_h1_data)


@pytest.fixture
def file_data_with_extra_d1_data(file_data):
    # D1: keep both days . H1: keep first day, remove second day
    file_data["data"]["EURUSD"]["raw_points_h1"] = file_data["data"]["EURUSD"][
        "raw_points_h1"
    ][0:2]
    return file_data


def test_extra_d1_data_raises_error(file_data_with_extra_d1_data):
    with pytest.raises(ValueError):
        InstrumentsSchema(**file_data_with_extra_d1_data)


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
    with pytest.raises(ValueError):
        InstrumentsSchema(**file_data_with_mismatched_end_dates)
