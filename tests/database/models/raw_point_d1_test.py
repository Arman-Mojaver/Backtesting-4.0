from database.models.raw_point_d1 import RawPointD1


def test_create_point(session):
    point_data = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point = RawPointD1(**point_data)

    session.add(point)
    session.commit()

    assert point.id
    assert point.to_dict() == point_data
