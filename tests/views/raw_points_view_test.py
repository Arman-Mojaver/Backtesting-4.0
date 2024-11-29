import pytest

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
