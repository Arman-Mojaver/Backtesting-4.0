import pytest

from database.models import ResampledPointD1
from fixtures.price_data import get_resampled_d1_data
from indicators.atr import get_atr_values, get_true_range_values
from utils.date_utils import string_to_datetime


@pytest.fixture
def resampled_points_d1(session):
    points_data_eurusd = get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-09-01"),
    )

    points = []
    for point_data in points_data_eurusd:
        point = ResampledPointD1(**point_data)
        points.append(point)

    session.add_all(points)
    session.commit()

    yield points

    for point in points:
        session.delete(point)

    session.commit()


TR_VALUES_2023_08_21__2023_09_01 = [
    1.09137 - 1.08634,
    max(1.09305 - 1.08329, abs(1.09305 - 1.08949), abs(1.08329 - 1.08949)),
    max(1.08715 - 1.08026, abs(1.08715 - 1.08452), abs(1.08026 - 1.08452)),
    max(1.08767 - 1.0805, abs(1.08767 - 1.08627), abs(1.0805 - 1.08627)),
    max(1.0842 - 1.07656, abs(1.0842 - 1.08096), abs(1.07656 - 1.08096)),
    max(1.08223 - 1.07928, abs(1.08223 - 1.07944), abs(1.07928 - 1.07944)),
    max(1.0892 - 1.07822, abs(1.0892 - 1.08182), abs(1.07822 - 1.08182)),
    max(1.09455 - 1.08551, abs(1.09455 - 1.08793), abs(1.08551 - 1.08793)),
    max(1.09394 - 1.08353, abs(1.09394 - 1.09227), abs(1.08353 - 1.09227)),
    max(1.08818 - 1.07715, abs(1.08818 - 1.08427), abs(1.07715 - 1.08427)),
]


def test_get_tr(resampled_points_d1):
    assert get_true_range_values(resampled_points_d1) == TR_VALUES_2023_08_21__2023_09_01


X = TR_VALUES_2023_08_21__2023_09_01


@pytest.mark.parametrize(
    ("atr_parameter", "expected_result"),
    [
        (
            2,
            [
                (X[0] + X[1]) / 2,
                (X[1] + X[2]) / 2,
                (X[2] + X[3]) / 2,
                (X[3] + X[4]) / 2,
                (X[4] + X[5]) / 2,
                (X[5] + X[6]) / 2,
                (X[6] + X[7]) / 2,
                (X[7] + X[8]) / 2,
                (X[8] + X[9]) / 2,
            ],
        ),
        (
            3,
            [
                (X[0] + X[1] + X[2]) / 3,
                (X[1] + X[2] + X[3]) / 3,
                (X[2] + X[3] + X[4]) / 3,
                (X[3] + X[4] + X[5]) / 3,
                (X[4] + X[5] + X[6]) / 3,
                (X[5] + X[6] + X[7]) / 3,
                (X[6] + X[7] + X[8]) / 3,
                (X[7] + X[8] + X[9]) / 3,
            ],
        ),
        (
            4,
            [
                (X[0] + X[1] + X[2] + X[3]) / 4,
                (X[1] + X[2] + X[3] + X[4]) / 4,
                (X[2] + X[3] + X[4] + X[5]) / 4,
                (X[3] + X[4] + X[5] + X[6]) / 4,
                (X[4] + X[5] + X[6] + X[7]) / 4,
                (X[5] + X[6] + X[7] + X[8]) / 4,
                (X[6] + X[7] + X[8] + X[9]) / 4,
            ],
        ),
        (
            5,
            [
                (X[0] + X[1] + X[2] + X[3] + X[4]) / 5,
                (X[1] + X[2] + X[3] + X[4] + X[5]) / 5,
                (X[2] + X[3] + X[4] + X[5] + X[6]) / 5,
                (X[3] + X[4] + X[5] + X[6] + X[7]) / 5,
                (X[4] + X[5] + X[6] + X[7] + X[8]) / 5,
                (X[5] + X[6] + X[7] + X[8] + X[9]) / 5,
            ],
        ),
        (
            6,
            [
                (X[0] + X[1] + X[2] + X[3] + X[4] + X[5]) / 6,
                (X[1] + X[2] + X[3] + X[4] + X[5] + X[6]) / 6,
                (X[2] + X[3] + X[4] + X[5] + X[6] + X[7]) / 6,
                (X[3] + X[4] + X[5] + X[6] + X[7] + X[8]) / 6,
                (X[4] + X[5] + X[6] + X[7] + X[8] + X[9]) / 6,
            ],
        ),
        (
            7,
            [
                (X[0] + X[1] + X[2] + X[3] + X[4] + X[5] + X[6]) / 7,
                (X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7]) / 7,
                (X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8]) / 7,
                (X[3] + X[4] + X[5] + X[6] + X[7] + X[8] + X[9]) / 7,
            ],
        ),
        (
            8,
            [
                (X[0] + X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7]) / 8,
                (X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8]) / 8,
                (X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8] + X[9]) / 8,
            ],
        ),
        (
            9,
            [
                (X[0] + X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8]) / 9,
                (X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8] + X[9]) / 9,
            ],
        ),
        (
            10,
            [
                (X[0] + X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8] + X[9])
                / 10,
            ],
        ),
    ],
)
def test_get_atr(atr_parameter, expected_result):
    assert (
        get_atr_values(TR_VALUES_2023_08_21__2023_09_01, atr_parameter) == expected_result
    )
