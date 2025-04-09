import pytest

from views.raw_points.utils import LoadFileData


def test_no_file_raises_error():
    with pytest.raises(FileNotFoundError):
        LoadFileData().run()


@pytest.fixture
def _setup_ignored_file(generate_file, file_data):
    generate_file(filename="random.json", data=file_data)


@pytest.mark.usefixtures("_setup_ignored_file")
def test_file_with_wrong_name_raises_error():
    with pytest.raises(FileNotFoundError):
        LoadFileData().run()


@pytest.fixture
def _setup_file_data(generate_file, file_data):
    generate_file(
        filename="20241126_2300_instrument_data.json",
        data=file_data,
    )


@pytest.mark.usefixtures("_setup_file_data")
def test_file_load_success(file_data):
    assert LoadFileData().run() == file_data
