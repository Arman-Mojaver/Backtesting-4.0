from copy import deepcopy

import pytest

DATA = {
    "data": {
        "EURUSD": {
            "raw_points_d1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13",
                    "high": 1.0706,
                    "instrument": "EURUSD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14",
                    "high": 1.08872,
                    "instrument": "EURUSD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
            "raw_points_h1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 00:00:00",
                    "high": 1.0706,
                    "instrument": "EURUSD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 01:00:00",
                    "high": 1.0706,
                    "instrument": "EURUSD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 00:00:00",
                    "high": 1.08872,
                    "instrument": "EURUSD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 01:00:00",
                    "high": 1.08872,
                    "instrument": "EURUSD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
        },
        "USDCAD": {
            "raw_points_d1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13",
                    "high": 1.0706,
                    "instrument": "USDCAD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14",
                    "high": 1.08872,
                    "instrument": "USDCAD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
            "raw_points_h1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 00:00:00",
                    "high": 1.0706,
                    "instrument": "USDCAD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 01:00:00",
                    "high": 1.0706,
                    "instrument": "USDCAD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 00:00:00",
                    "high": 1.08872,
                    "instrument": "USDCAD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 01:00:00",
                    "high": 1.08872,
                    "instrument": "USDCAD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
        },
    }
}


@pytest.fixture()
def file_data():
    return deepcopy(DATA)
