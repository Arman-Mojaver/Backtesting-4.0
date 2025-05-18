import json
import os
from copy import deepcopy
from pathlib import Path

import pytest

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config  # type: ignore[attr-defined]
from database.models import Indicator, MoneyManagementStrategy

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"


@pytest.fixture
def rust_server():
    """Equivalent to calling "localhost" from outside the container."""
    return "http://host.docker.internal:81"


@pytest.fixture
def rust_endpoint(rust_server):
    def _endpoint(url):
        return f"{rust_server}/{url}"

    return _endpoint


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


@pytest.fixture
def generate_file():
    def _generate_file(filename, data):
        path = Path(project_config.INSTRUMENT_DATA_PATH) / filename

        with path.open("w") as f:
            json.dump(data, f)

    yield _generate_file

    folder = Path(project_config.INSTRUMENT_DATA_PATH)
    for file_path in folder.glob("*"):
        if file_path.is_file() and not str(file_path).endswith(".gitkeep"):
            file_path.unlink()


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
        "identifier": "atr-0.4-0.2-3",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy(money_management_strategy_data):
    return MoneyManagementStrategy(id=101, **money_management_strategy_data)


@pytest.fixture
def money_management_strategy_data_2():
    return {
        "type": "atr",
        "tp_multiplier": 0.6,
        "sl_multiplier": 0.3,
        "parameters": {"atr_parameter": 3},
        "identifier": "atr-0.6-0.3-3",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy_2(money_management_strategy_data_2):
    return MoneyManagementStrategy(id=102, **money_management_strategy_data_2)


@pytest.fixture
def money_management_strategies(money_management_strategy, money_management_strategy_2):
    return [money_management_strategy, money_management_strategy_2]


@pytest.fixture
def indicator_data():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }


@pytest.fixture
def indicator_data_2():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 13, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-13-close,ema-5-close",
    }


@pytest.fixture
def indicator(indicator_data):
    return Indicator(**indicator_data)


@pytest.fixture
def indicator_2(indicator_data_2):
    return Indicator(**indicator_data_2)
